from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import Client

from notes.models import Note


User = get_user_model()


class SetUpTestDataClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url_notes_home = reverse('notes:home')
        cls.url_notes_list = reverse('notes:list')
        cls.url_notes_add = reverse('notes:add')
        cls.url_notes_success = reverse('notes:success')
        cls.url_users_login = reverse('users:login')
        cls.url_users_logout = reverse('users:logout')
        cls.url_users_signup = reverse('users:signup')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст',
                                       author=cls.author)
        cls.url_notes_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_notes_detail = reverse('notes:detail', args=(cls.note.slug,))
        cls.url_notes_delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.guest_client = Client()
