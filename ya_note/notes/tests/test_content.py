from notes.forms import NoteForm
from .common import SetUp


class TestHomePage(SetUp):

    def test_notes_list_for_different_users(self):
        """Тест доступности листа заметок для автора и не автора"""
        param = ((self.author, True), (self.reader, False))
        for user, note_in_list in param:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(self.url_notes_list)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        self.client.force_login(self.author)
        for url in (self.url_notes_add, self.url_notes_edit):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
