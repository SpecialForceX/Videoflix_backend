@echo off
echo Starte FFmpeg-Konvertierung zu HLS...

mkdir "media\videos\hls\ufo" 2>nul

ffmpeg -i media/videos/ufo.mp4 ^
-filter_complex "[0:v]split=3[v1][v2][v3]; [v1]scale=w=854:h=480[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=1920:h=1080[v3out]" ^
-map "[v1out]" -c:v:0 libx264 -b:v:0 800k -maxrate:v:0 856k -bufsize:v:0 1200k ^
-map "[v2out]" -c:v:1 libx264 -b:v:1 1400k -maxrate:v:1 1498k -bufsize:v:1 2100k ^
-map "[v3out]" -c:v:2 libx264 -b:v:2 2800k -maxrate:v:2 2996k -bufsize:v:2 4200k ^
-f hls ^
-var_stream_map "v:0 v:1 v:2" ^
-master_pl_name master.m3u8 ^
-hls_time 10 ^
-hls_list_size 0 ^
-hls_segment_filename "media/videos/hls/ufo/%%v_%%03d.ts" ^
"media/videos/hls/ufo/%%v.m3u8"

echo ✅ HLS-Streams wurden erfolgreich generiert!
pause





