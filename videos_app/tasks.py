import os
import subprocess
from django.conf import settings
from .models import Video
from django_rq import job

RESOLUTIONS = {
    '480p': '854x480',
    '720p': '1280x720',
    '1080p': '1920x1080',
}



@job('default', timeout=None)
def transcode_video(video_id):
    """
    Background job to transcode a video into HLS format with multiple resolutions.

    This function uses FFMPEG to transcode the input video into three quality levels:
    480p, 720p, and 1080p. It generates `.m3u8` playlist files and `.ts` segment files 
    for each resolution and a master playlist to combine them.

    Args:
        video_id (int): The ID of the video to be transcoded.

    Side Effects:
        - Creates HLS output directory and files on disk.
        - Logs process output to the console.

    Returns:
        None
    """
    video = Video.objects.get(id=video_id)
    input_path = video.video_file.path

    filename = os.path.splitext(os.path.basename(input_path))[0]
    hls_dir = os.path.join(os.path.dirname(input_path), 'hls', filename)
    os.makedirs(hls_dir, exist_ok=True)

    # Zielpfad für .m3u8 Master Playlist
    master_playlist_path = os.path.join(hls_dir, 'master.m3u8')

    # FFMPEG Befehl aufbauen
    command = [
        'ffmpeg',
        '-i', input_path,
        '-filter_complex', '[0:v]split=3[v1][v2][v3]; [v1]scale=w=854:h=480[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=1920:h=1080[v3out]',
        '-map', '[v1out]', '-map', 'a:0', '-c:v:0', 'libx264', '-b:v:0', '800k', '-maxrate:v:0', '856k', '-bufsize:v:0', '1200k', '-c:a:0', 'aac', '-b:a:0', '128k',
        '-map', '[v2out]', '-map', 'a:0', '-c:v:1', 'libx264', '-b:v:1', '1400k', '-maxrate:v:1', '1498k', '-bufsize:v:1', '2100k', '-c:a:1', 'aac', '-b:a:1', '128k',
        '-map', '[v3out]', '-map', 'a:0', '-c:v:2', 'libx264', '-b:v:2', '2800k', '-maxrate:v:2', '2996k', '-bufsize:v:2', '4200k', '-c:a:2', 'aac', '-b:a:2', '128k',
        '-f', 'hls',
        '-var_stream_map', 'v:0,a:0 v:1,a:1 v:2,a:2',
        '-master_pl_name', 'master.m3u8',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-hls_segment_filename', os.path.join(hls_dir, '%v_%03d.ts'),
        os.path.join(hls_dir, '%v.m3u8')
    ]

    print(f"🔁 Starte Transcoding zu HLS: {filename}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"❌ Fehler beim Transcoding: {result.stderr.decode()}")
    else:
        print(f"✅ Transcoding abgeschlossen für Video ID {video.id}")

