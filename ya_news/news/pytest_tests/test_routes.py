from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_news_home'),
        pytest.lazy_fixture('url_news_detail'),
        pytest.lazy_fixture('url_news_edit'),
        pytest.lazy_fixture('url_news_delete'),
        pytest.lazy_fixture('url_users_login'),
        pytest.lazy_fixture('url_users_logout'),
        pytest.lazy_fixture('url_users_signup'),
    )
)
def test_pages_availability(
    url, parametrized_client, expected_status, not_author_client,
    url_news_edit, url_news_delete
):
    if ((parametrized_client == not_author_client)
        and (url == url_news_edit or url == url_news_delete
             )):
        expected_status = HTTPStatus.NOT_FOUND
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_news_edit'),
        pytest.lazy_fixture('url_news_delete'),
    ),
)
def test_redirect_for_anonymous_client(client, url, url_users_login):
    expected_url = f'{url_users_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
