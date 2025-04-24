from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from videos_app.models import Video
from .serializers import VideoSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import VideoDetailSerializer

class VideoDashboardView(APIView):
    """
    API view to retrieve a list of all videos for the dashboard.

    Only accessible to authenticated users. Videos are returned in reverse 
    chronological order and include related genre information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return a serialized list of all videos.

        Returns:
            Response: A list of serialized video data.
        """
        videos = Video.objects.select_related('genre').order_by('-created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class VideoDetailView(RetrieveAPIView):
    """
    API view to retrieve detailed information about a single video.

    Only accessible to authenticated users. Fetches the video along with its genre.
    """
    queryset = Video.objects.select_related('genre').all()
    serializer_class = VideoDetailSerializer
    permission_classes = [IsAuthenticated]
