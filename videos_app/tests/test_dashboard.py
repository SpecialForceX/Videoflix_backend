import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users_app.models import CustomUser

@pytest.mark.django_db
def test_dashboard_returns_empty_list_for_authenticated_user():
    user = CustomUser.objects.create_user(email="viewer@test.com", password="securepass123", is_active=True)
    client = APIClient()
    login = client.post(reverse('token_obtain_pair'), {
        "email": "viewer@test.com",
        "password": "securepass123"
    })

    token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse('video-dashboard'))

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0

@pytest.mark.django_db
def test_dashboard_requires_authentication():
    client = APIClient()
    response = client.get(reverse('video-dashboard'))

    assert response.status_code == 401
