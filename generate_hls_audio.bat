@echo off
echo Starte HLS-Konvertierung für pilz.mp4...

set "filename=pilz"

mkdir "media\videos\hls\%filename%" 2>nul

ffmpeg -i "media/videos/%filename%.mp4" ^
-filter_complex "[0:v]split=3[v1][v2][v3]; [v1]scale=w=854:h=480[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=1920:h=1080[v3out]" ^
-map "[v1out]" -map a:0 -c:v:0 libx264 -b:v:0 800k -maxrate:v:0 856k -bufsize:v:0 1200k -c:a:0 aac -b:a:0 128k ^
-map "[v2out]" -map a:0 -c:v:1 libx264 -b:v:1 1400k -maxrate:v:1 1498k -bufsize:v:1 2100k -c:a:1 aac -b:a:1 128k ^
-map "[v3out]" -map a:0 -c:v:2 libx264 -b:v:2 2800k -maxrate:v:2 2996k -bufsize:v:2 4200k -c:a:2 aac -b:a:2 128k ^
-f hls ^
-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" ^
-master_pl_name master.m3u8 ^
-hls_time 10 ^
-hls_list_size 0 ^
-hls_segment_filename "media/videos/hls/%filename%/%%v_%%03d.ts" ^
"media/videos/hls/%filename%/%%v.m3u8"

echo ✅ pilz.mp4 fertig konvertiert!
pause

