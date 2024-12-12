from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .common import SetUpTestDataClass


class TestCommentCreation(SetUpTestDataClass):

    def test_user_can_create_note(self):
        """Тест возможности создания заметки автором"""
        note_count_old = Note.objects.count()
        response = self.author_client.post(self.url_notes_add,
                                           data=self.form_data)
        self.assertRedirects(response, self.url_notes_success)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_new - note_count_old, 1)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Тест не возможности создания заметки гостем"""
        note_count_old = Note.objects.count()
        response = self.client.post(self.url_notes_add, data=self.form_data)
        expected_url = f'{self.url_users_login}?next={self.url_notes_add}'
        self.assertRedirects(response, expected_url)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new)

    def test_not_unique_slug(self):
        """Тест на уникальность слага"""
        note_count_old = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.url_notes_add,
                                           data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(self.note.slug + WARNING)
        )
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new)

    def test_empty_slug(self):
        """Тест создания заметки с пустым слагом"""
        note_count_old = Note.objects.count()
        self.form_data.pop('slug')
        response = self.author_client.post(self.url_notes_add,
                                           data=self.form_data)
        self.assertRedirects(response, self.url_notes_success)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old + 1, note_count_new)
        new_note = Note.objects.get(id=note_count_old + 1)
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Тест возможности изменения заметки автором"""
        note_count_old = Note.objects.count()
        response = self.author_client.post(self.url_notes_edit, self.form_data)
        self.assertRedirects(response, self.url_notes_success)
        self.note = Note.objects.get(id=self.note.id)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new)
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        """Тест не возможности изменения заметки гостем"""
        note_count_old = Note.objects.count()
        response = self.client.post(self.url_notes_edit, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        """Тест возможности удаления заметки автором"""
        note_count_old = Note.objects.count()
        response = self.author_client.post(self.url_notes_delete)
        self.assertRedirects(response, self.url_notes_success)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new + 1)

    def test_other_user_cant_delete_note(self):
        """Тест не возможности удаления заметки гостем"""
        note_count_old = Note.objects.count()
        response = self.client.post(self.url_notes_delete)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note_count_new = Note.objects.count()
        self.assertEqual(note_count_old, note_count_new)
