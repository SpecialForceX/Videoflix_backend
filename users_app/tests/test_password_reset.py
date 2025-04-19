import pytest
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient
from users_app.models import CustomUser

@pytest.mark.django_db
def test_password_reset_request_returns_200():
    user = CustomUser.objects.create_user(email='reset@test.com', password='test123', is_active=True)
    client = APIClient()

    response = client.post(reverse('password_reset_request'), {"email": "reset@test.com"})
    
    assert response.status_code == 200
    assert "detail" in response.data

@pytest.mark.django_db
def test_password_reset_successful():
    user = CustomUser.objects.create_user(email='reset2@test.com', password='test123', is_active=True)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    client = APIClient()
    url = reverse('password_reset_confirm', kwargs={"uidb64": uid, "token": token})
    response = client.post(url, {
        "password": "newsecurepassword123",
        "password2": "newsecurepassword123"
    })

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("newsecurepassword123")

@pytest.mark.django_db
def test_password_reset_fails_with_invalid_token():
    user = CustomUser.objects.create_user(email='reset3@test.com', password='test123', is_active=True)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    invalid_token = "invalid-token-123"

    client = APIClient()
    url = reverse('password_reset_confirm', kwargs={"uidb64": uid, "token": invalid_token})
    response = client.post(url, {
        "password": "pass12345",
        "password2": "pass12345"
    })

    assert response.status_code == 400
    assert "detail" in response.data
