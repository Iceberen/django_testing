from http import HTTPStatus

from .common import SetUpTestDataClass


class TestRoutes(SetUpTestDataClass):

    def test_pages_availability(self):
        """Тест доступности страниц"""
        urls = (
            self.url_notes_home,
            self.url_users_login,
            self.url_users_logout,
            self.url_users_signup,
            self.url_notes_list,
            self.url_notes_add,
            self.url_notes_success,
            self.url_notes_detail,
            self.url_notes_edit,
            self.url_notes_delete,
        )

        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.OK),
            (None, HTTPStatus.OK),
        )

        for user, status in users_statuses:
            for url in urls:
                with self.subTest(user=user):
                    if user is not None:
                        self.client.force_login(user)
                    if (user == self.reader
                        and (url == self.url_notes_edit
                             or url == self.url_notes_detail)):
                        status = HTTPStatus.NOT_FOUND
                    if user is None and url in (urls[4:]):
                        status = HTTPStatus.FOUND
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        """Тест редиректов"""
        urls = (
            self.url_notes_detail,
            self.url_notes_edit,
            self.url_notes_delete,
            self.url_notes_add,
            self.url_notes_success,
            self.url_notes_list,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.url_users_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
