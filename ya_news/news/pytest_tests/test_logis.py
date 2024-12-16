from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


DATA_FORM = {'text': 'Текст комментария'}
DATA_FORM_NEW = {'text': 'New comm'}


def test_anonymous_user_cant_create_comment(client, url_news_detail):
    comments_count_old = Comment.objects.count()
    client.post(url_news_detail, data=DATA_FORM)
    comments_count_new = Comment.objects.count()
    assert comments_count_old == comments_count_new


def test_user_can_create_comment(news, author, author_client, url_news_detail):
    comments_count_old = Comment.objects.count()
    list_id_old = list(Comment.objects.values_list('id'))
    response = author_client.post(url_news_detail, data=DATA_FORM)
    assertRedirects(response, f'{url_news_detail}#comments')
    list_id_new = list(Comment.objects.values_list('id', flat=True))
    comments_count_new = Comment.objects.count()
    assert comments_count_old + 1 == comments_count_new
    assert len(list_id_new) - len(list_id_old) == 1
    new_comment_id = list(set(list_id_new) - set(list_id_old))[0]
    comment = Comment.objects.get(id=new_comment_id)
    assert comment.text == DATA_FORM['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, url_news_detail):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    comments_count_old = Comment.objects.count()
    response = author_client.post(url_news_detail, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count_new = Comment.objects.count()
    assert comments_count_old == comments_count_new


def test_author_can_delete_comment(author_client, url_news_delete,
                                   url_news_detail, comment):
    comments_count_old = Comment.objects.count()
    response = author_client.delete(url_news_delete)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count_new = Comment.objects.count()
    assert comments_count_old - 1 == comments_count_new
    assert (Comment.objects.filter(id=comment.id).exists() is False)


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, news, author, url_news_delete
):
    comments_count_old = Comment.objects.count()
    response = not_author_client.delete(url_news_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count_new = Comment.objects.count()
    assert comments_count_old == comments_count_new
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == DATA_FORM['text']
    assert comment.news == news
    assert comment.author == author


def test_author_can_edit_comment(author, author_client, news, comment,
                                 url_news_detail, url_news_edit):
    comments_count_old = Comment.objects.count()
    response = author_client.post(url_news_edit, data=DATA_FORM_NEW)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment = Comment.objects.get(id=comment.id)
    comments_count_new = Comment.objects.count()
    assert comments_count_old == comments_count_new
    assert comment.text == DATA_FORM_NEW['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, url_news_edit
):
    comments_count_old = Comment.objects.count()
    response = not_author_client.post(url_news_edit, data=DATA_FORM_NEW)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count_new = Comment.objects.count()
    assert comments_count_old == comments_count_new
    last_comment = Comment.objects.get(id=comment.id)
    assert last_comment.text == comment.text
    assert last_comment.news == comment.news
    assert last_comment.author == comment.author
