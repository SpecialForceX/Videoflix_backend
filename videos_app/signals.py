# videos_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq

from .models import Video
from .tasks import transcode_video

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default')
        queue.enqueue(transcode_video, instance.id)
