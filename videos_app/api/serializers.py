from rest_framework import serializers
from videos_app.models import Video, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'genre', 'thumbnail', 'video_file', 'created_at']

class VideoDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'genre', 'thumbnail', 'video_file', 'created_at']

