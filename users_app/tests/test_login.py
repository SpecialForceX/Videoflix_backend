import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users_app.models import CustomUser

LOGIN_URL = reverse('token_obtain_pair')

@pytest.mark.django_db
def test_login_successfully_with_valid_credentials():
    user = CustomUser.objects.create_user(email='login@test.com', password='securepass123', is_active=True)
    client = APIClient()

    response = client.post(LOGIN_URL, {
        "email": "login@test.com",
        "password": "securepass123"
    })

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_fails_with_wrong_password():
    user = CustomUser.objects.create_user(email='wrongpass@test.com', password='securepass123', is_active=True)
    client = APIClient()

    response = client.post(LOGIN_URL, {
        "email": "wrongpass@test.com",
        "password": "falsch123"
    })

    assert response.status_code == 401
    assert "access" not in response.data

@pytest.mark.django_db
def test_login_fails_if_user_not_active():
    user = CustomUser.objects.create_user(email='inactive@test.com', password='securepass123', is_active=False)
    client = APIClient()

    response = client.post(LOGIN_URL, {
        "email": "inactive@test.com",
        "password": "securepass123"
    })

    assert response.status_code == 401
