import subprocess
import os

def transcode_resolutions(input_path, output_base):
    resolutions = {
        '1080p': '1920x1080',
        '720p': '1280x720',
        '480p': '854x480',
    }

    for label, size in resolutions.items():
        output_path = f"{output_base}_{label}.mp4"
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={size}',
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'fast',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ]
        print(f"Creating {label} version...")
        subprocess.run(cmd, check=True)
