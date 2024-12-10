from http import HTTPStatus

from .common import SetUp


class TestRoutes(SetUp):

    def test_pages_availability(self):
        urls_anonym = (
            (self.url_notes_home, HTTPStatus.OK),
            (self.url_users_login, HTTPStatus.OK),
            (self.url_users_logout, HTTPStatus.OK),
            (self.url_users_signup, HTTPStatus.OK),
        )
        for url, status in urls_anonym:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

        urls_auth = (
            (self.url_notes_list, HTTPStatus.OK),
            (self.url_notes_add, HTTPStatus.OK),
            (self.url_notes_success, HTTPStatus.OK),
        )
        self.client.force_login(self.author)
        for url, status in urls_auth:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        url_diff = (
            self.url_notes_detail,
            self.url_notes_edit,
            self.url_notes_delete,
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in url_diff:
                with self.subTest(url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
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
