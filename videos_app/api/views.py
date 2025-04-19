from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from videos_app.models import Video
from .serializers import VideoSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import VideoDetailSerializer

class VideoDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.select_related('genre').order_by('-created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class VideoDetailView(RetrieveAPIView):
    queryset = Video.objects.select_related('genre').all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated]
