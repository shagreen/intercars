from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.factories import UserFactory


@pytest.mark.django_db
def test_login_user_api():
    """Api user/login endpoint unit test"""
    # Given
    client = APIClient()
    password = "kekemeke"
    test_user = UserFactory(password=password)

    # When
    response = client.post(
        '/users/login/',
        {
            "username": test_user.username,
            "password": password
        },
        format="json"
    )
    # Then
    token = Token.objects.get(user=test_user)
    assert response.json() == {
        'key': token.key
    }


@pytest.mark.django_db
def test_logout_user_api():
    """Api user/logout endpoint unit test"""
    # Given
    client = APIClient()
    password = "kekemeke"
    test_user = UserFactory(password=password)
    response = client.post(
        '/users/login/',
        {
            "username": test_user.username,
            "password": password
        },
        format="json"
    )
    # When
    client.credentials(HTTP_AUTHORIZATION='Token ' + response.json().get('key'))
    client.post(
        '/users/logout/',
        format="json"
    )
    # Then
    assert Token.objects.filter(user=test_user).exists() is False


@pytest.mark.django_db
def test_token_expiration():
    """Api token expiration unit test"""
    # Given
    client = APIClient()
    password = "kekemeke"
    test_user = UserFactory(password=password)

    response = client.post(
        '/users/login/',
        {
            "username": test_user.username,
            "password": password
        },
        format="json"
    )
    client.credentials(HTTP_AUTHORIZATION='Token ' + response.json().get('key'))
    # When
    with freeze_time(datetime.now() + timedelta(days=settings.TOKEN_EXPIRATION_DAYS) + timedelta(days=1)):
        response = client.post(
            '/users/login/',
            {
                "username": test_user.username,
                "password": password
            },
            format="json"
        )

    # Then
    assert response.status_code == 401, "Wrong status code after token expiration!"
    assert response.json() == {'detail': _('Token has expired')}, "Wrong response detail!"
