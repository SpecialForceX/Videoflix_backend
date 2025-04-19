import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users_app.models import CustomUser

@pytest.mark.django_db
def test_user_can_register_successfully():
    client = APIClient()
    payload = {
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    }
    response = client.post(reverse('user-register'), data=payload)
    assert response.status_code == 201
    assert CustomUser.objects.filter(email="test@example.com").exists()
    user = CustomUser.objects.get(email="test@example.com")
    assert user.is_active is False  # Muss erst aktiviert werden

@pytest.mark.django_db
def test_registration_with_mismatched_passwords():
    client = APIClient()
    payload = {
        "email": "wrong@example.com",
        "password": "testpass123",
        "password2": "wrongpass456"
    }
    response = client.post(reverse('user-register'), data=payload)
    assert response.status_code == 400
