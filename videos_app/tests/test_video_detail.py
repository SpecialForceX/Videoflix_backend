import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users_app.models import CustomUser
from videos_app.models import Video, Genre
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_authenticated_user_can_get_video_detail():
    user = CustomUser.objects.create_user(email="user@test.com", password="secure123", is_active=True)
    genre = Genre.objects.create(name="Action")
    video = Video.objects.create(
        title="Test Video",
        description="Test Beschreibung",
        genre=genre,
        thumbnail=SimpleUploadedFile("thumb.jpg", b"filedata", content_type="image/jpeg"),
        video_file=SimpleUploadedFile("video.mp4", b"videodata", content_type="video/mp4")
    )

    client = APIClient()
    login = client.post(reverse('token_obtain_pair'), {
        "email": "user@test.com",
        "password": "secure123"
    })
    token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse('video-detail', kwargs={"pk": video.pk}))
    assert response.status_code == 200
    assert response.data["title"] == "Test Video"
    assert response.data["genre"]["name"] == "Action"

@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_video_detail():
    response = APIClient().get(reverse('video-detail', kwargs={"pk": 1}))
    assert response.status_code == 401

@pytest.mark.django_db
def test_authenticated_user_gets_404_on_invalid_video_id():
    user = CustomUser.objects.create_user(email="user404@test.com", password="secure123", is_active=True)
    client = APIClient()
    login = client.post(reverse('token_obtain_pair'), {
        "email": "user404@test.com",
        "password": "secure123"
    })
    token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse('video-detail', kwargs={"pk": 999}))
    assert response.status_code == 404
