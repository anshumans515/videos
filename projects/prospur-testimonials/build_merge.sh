#!/usr/bin/env bash
# Merge the Prospur testimonial clips into one 1080x1920 / 30fps video.
#
# ORDER is fixed by the client: upload order for the body, then the three
# named positions at the end — third-last, Aseem second-last, Vedant last.
#
# TWO THINGS THAT WOULD SILENTLY WRECK THIS IF UNHANDLED
#
# 1. ROTATION. Four sources carry a rotation side-data flag, so the stored
#    width/height do NOT describe the decoded frame:
#      05, 12  stored 1024x576  -> decode 576x1024  (portrait)
#      11      stored 576x1024  -> decode 1024x576  (landscape)
#      02, 07, 10 are rot=-180 (upright after auto-rotation, but flagged)
#    Deciding portrait-vs-landscape from ffprobe's stored dimensions would
#    put three clips through the wrong branch. This script asks ffmpeg for
#    the DECODED size instead, which is what the filters actually receive.
#
# 2. MIXED LOUDNESS. Sources range -16.9 to -38.3 LUFS. Concatenating them
#    raw means the viewer rides the volume knob for 13 minutes. Every
#    segment is normalised to -14 LUFS / -1.5 dBTP first.
#
# Landscape clips are NOT centre-cropped to 9:16 — that would throw away
# ~68% of the frame width and cut off the speakers' hands. They sit in a
# centred band over a blurred, darkened copy of themselves instead.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
UPLOADS="${1:?path to the uploads directory}"
W=1080; H=1920; FPS=30
SEG="$HERE/segments"
mkdir -p "$SEG" "$HERE/public"

# order = final running order. Body in upload order, then the named tail.
read -r -d '' ORDER <<'EOF' || true
01 7999291c-VID20260805WA0001.mp4
02 4dc2973b-VID20260804WA0022.mp4
03 98e1f379-VID20260804WA0010.mp4
04 bd0b4c44-VID20260805WA0003.mp4
05 b09e2701-VID20260802WA0022.mp4
06 a3ff45e5-VID20260802WA0034.mp4
07 42576fd6-VID20260805WA0020.mp4
08 ef19197f-VID20260804WA0015.mp4
09 4203526b-VID20260802WA0002.mp4
10 bc75f720-VID20260803WA0008.mp4
11 cda2f5da-VID20260804WA0003.mp4
12 b45b340c-WhatsApp_Video_20260807_at_14.07.02.mp4
13 ce447f84-aseem.mp4
14 4908663c-vedant2.mp4
EOF

: > "$HERE/concat.txt"

while read -r n f; do
  [ -z "${n:-}" ] && continue
  src="$UPLOADS/$f"
  [ -f "$src" ] || { echo "MISSING: $src" >&2; exit 1; }

  # Decoded (post-rotation) size — the only size that describes reality.
  ffmpeg -nostdin -v error -ss 1 -i "$src" -frames:v 1 -y "$SEG/.probe.png"
  read -r dw dh < <(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$SEG/.probe.png" | tr ',' ' ')
  rm -f "$SEG/.probe.png"

  if [ "$dh" -ge "$dw" ]; then
    # Portrait: fill the frame, crop the overflow.
    VF="scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H}"
    mode="portrait fill"
  else
    # Landscape: centred band over a blurred, darkened copy of itself.
    VF="split=2[bg][fg];\
[bg]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},gblur=sigma=30,eq=brightness=-0.13:saturation=0.85[bgo];\
[fg]scale=${W}:-2[fgo];\
[bgo][fgo]overlay=(W-w)/2:(H-h)/2"
    mode="landscape + blurred bed"
  fi

  echo ">> $n ($f)  decoded ${dw}x${dh}  -> $mode"
  ffmpeg -nostdin -v error -y -i "$src" \
    -filter_complex "[0:v]fps=${FPS},${VF},format=yuv420p[v]" \
    -filter_complex_threads 1 \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" \
    -map "[v]" -map 0:a:0 \
    -c:v libx264 -preset veryfast -crf 24 -g 60 -keyint_min 60 -pix_fmt yuv420p \
    -c:a aac -b:a 128k -ac 2 -ar 48000 \
    -video_track_timescale 30000 \
    "$SEG/seg_${n}.mp4"

  echo "file '$SEG/seg_${n}.mp4'" >> "$HERE/concat.txt"
done <<< "$ORDER"

echo ">> concatenating"
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$HERE/concat.txt" \
  -c copy -movflags +faststart "$HERE/public/testimonials-merged.mp4"

echo "--- result ---"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate \
  -show_entries format=duration,size -of default=noprint_wrappers=1 \
  "$HERE/public/testimonials-merged.mp4"
echo "--- loudness ---"
ffmpeg -nostats -i "$HERE/public/testimonials-merged.mp4" -af ebur128=peak=true -f null - 2>&1 \
  | grep -E "^ +(I|Peak):"
