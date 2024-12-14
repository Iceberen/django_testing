from http import HTTPStatus

from .common import SetUpTestDataClass


class TestRoutes(SetUpTestDataClass):

    def test_pages_availability(self):
        """Тест доступности страниц"""
        client_urls_status = (
            (self.author, self.url_notes_home, HTTPStatus.OK),
            (self.author, self.url_users_login, HTTPStatus.OK),
            (self.author, self.url_users_logout, HTTPStatus.OK),
            (self.author, self.url_users_signup, HTTPStatus.OK),
            (self.author, self.url_notes_list, HTTPStatus.OK),
            (self.author, self.url_notes_add, HTTPStatus.OK),
            (self.author, self.url_notes_success, HTTPStatus.OK),
            (self.author, self.url_notes_detail, HTTPStatus.OK),
            (self.author, self.url_notes_edit, HTTPStatus.OK),
            (self.author, self.url_notes_delete, HTTPStatus.OK),
            (self.reader, self.url_notes_home, HTTPStatus.OK),
            (self.reader, self.url_users_login, HTTPStatus.OK),
            (self.reader, self.url_users_logout, HTTPStatus.OK),
            (self.reader, self.url_users_signup, HTTPStatus.OK),
            (self.reader, self.url_notes_list, HTTPStatus.OK),
            (self.reader, self.url_notes_add, HTTPStatus.OK),
            (self.reader, self.url_notes_success, HTTPStatus.OK),
            (self.reader, self.url_notes_detail, HTTPStatus.NOT_FOUND),
            (self.reader, self.url_notes_edit, HTTPStatus.NOT_FOUND),
            (self.reader, self.url_notes_delete, HTTPStatus.NOT_FOUND),
            (self.client, self.url_notes_home, HTTPStatus.OK),
            (self.client, self.url_users_login, HTTPStatus.OK),
            (self.client, self.url_users_logout, HTTPStatus.OK),
            (self.client, self.url_users_signup, HTTPStatus.OK),
            (self.client, self.url_notes_list, HTTPStatus.FOUND),
            (self.client, self.url_notes_add, HTTPStatus.FOUND),
            (self.client, self.url_notes_success, HTTPStatus.FOUND),
            (self.client, self.url_notes_detail, HTTPStatus.FOUND),
            (self.client, self.url_notes_edit, HTTPStatus.FOUND),
            (self.client, self.url_notes_delete, HTTPStatus.FOUND),
        )

        for user, url, status in client_urls_status:
            with self.subTest(user=user):
                if user is not self.client:
                    self.client.force_login(user)
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
