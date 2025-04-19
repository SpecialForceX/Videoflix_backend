import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from users_app.models import CustomUser
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_activation_with_valid_token():
    user = CustomUser.objects.create_user(email='toactivate@example.com', password='pass123')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    client = APIClient()
    url = reverse('user-activate', kwargs={"uidb64": uid, "token": token})
    response = client.get(url)
    user.refresh_from_db()

    assert response.status_code == 200
    assert user.is_active is True

@pytest.mark.django_db
def test_activation_with_invalid_token():
    user = CustomUser.objects.create_user(email='invalid@example.com', password='pass123')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = 'invalid-token'

    client = APIClient()
    url = reverse('user-activate', kwargs={"uidb64": uid, "token": token})
    response = client.get(url)
    user.refresh_from_db()

    assert response.status_code == 400
    assert user.is_active is False
