from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.test.client import Client


@pytest.mark.parametrize(
    'parametrized_client, url, expected_status',
    (
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_news_home'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_news_detail'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_news_edit'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_news_delete'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_users_login'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_users_logout'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('url_users_signup'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_news_home'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_news_detail'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_news_edit'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_news_delete'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_users_login'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_users_logout'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('url_users_signup'),
            HTTPStatus.OK
        ),
        (
            Client(),
            pytest.lazy_fixture('url_news_home'),
            HTTPStatus.OK
        ),
        (
            Client(),
            pytest.lazy_fixture('url_news_detail'),
            HTTPStatus.OK
        ),
        (
            Client(),
            pytest.lazy_fixture('url_news_edit'),
            HTTPStatus.FOUND
        ),
        (
            Client(),
            pytest.lazy_fixture('url_news_delete'),
            HTTPStatus.FOUND
        ),
        (
            Client(),
            pytest.lazy_fixture('url_users_login'),
            HTTPStatus.OK
        ),
        (
            Client(),
            pytest.lazy_fixture('url_users_logout'),
            HTTPStatus.OK
        ),
        (
            Client(),
            pytest.lazy_fixture('url_users_signup'),
            HTTPStatus.OK
        ),
    ),
)
def test_pages_availability(
    parametrized_client, url, expected_status, not_author_client,
    url_news_edit, url_news_delete, client
):
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
