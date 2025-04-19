from django.urls import path
from .views import VideoDashboardView, VideoDetailView

urlpatterns = [
    path('', VideoDashboardView.as_view(), name='video-dashboard'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
