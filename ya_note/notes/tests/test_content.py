from notes.forms import NoteForm
from .common import SetUpTestDataClass
from http import HTTPStatus


class TestHomePage(SetUpTestDataClass):

    def test_notes_list_for_different_users(self):
        """Тест доступности листа заметок для автора и не автора"""
        response = self.author_client.get(self.url_notes_list)
        object_list = response.context['object_list']
        self.assertEqual((self.note in object_list), True)
        response2 = self.client.get(self.url_notes_list)
        self.assertEqual(response2.status_code, HTTPStatus.FOUND)

    def test_pages_contains_form(self):
        """Тест на наличие формы заметки"""
        for url in (self.url_notes_add, self.url_notes_edit):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
