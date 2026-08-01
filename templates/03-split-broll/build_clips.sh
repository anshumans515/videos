#!/usr/bin/env bash
# Split-screen B-roll build (PLAYBOOK.md §8). Produces public/input-video.mp4:
# two source clips -> 540x1920 halves -> hstack -> mux music bed.
#
# Tune every *_ss/*_to/setpts/crop value per source clip — these are
# starting points, not defaults that work unmodified. In particular retune
# `crop iw*0.22` / `crop iw*0.28` so each half is centered on the subject,
# not the background (§8).
#
# Usage: ./build_clips.sh <source-with-saver-segment.mp4> <source-with-spender-segment.mp4> <music_bed.m4a>
set -euo pipefail

SAVER_SRC="${1:?saver source clip}"
SPENDER_SRC="${2:?spender source clip}"
MUSIC_BED="${3:?music bed (m4a/aac)}"

OUT_DURATION=25.5

# --- LEFT (SAVER / positive side) --------------------------------------
# Slow-loop one clean segment so the character stays consistent (§8).
# Adjust -ss/-to to a clean 1.5-2s segment of the person in the source.
ffmpeg -y -ss 20.7 -to 22.5 -i "$SAVER_SRC" -an \
  -vf "eq=brightness=0.05:contrast=1.05:saturation=1.08:gamma=1.06,setpts=5.5*PTS" -r 30 saver.mp4
ffmpeg -y -stream_loop -1 -i saver.mp4 -t "$OUT_DURATION" saver_loop.mp4

# --- RIGHT (SPENDER / negative side) ------------------------------------
# The montage part of the source. Adjust -to and setpts to fit OUT_DURATION.
ffmpeg -y -ss 0 -to 19 -i "$SPENDER_SRC" -an \
  -vf "eq=brightness=0.05:contrast=1.05:saturation=1.08:gamma=1.06,setpts=1.34*PTS,trim=duration=${OUT_DURATION}" \
  -r 30 spender.mp4

# --- Stitch + mux music bed ----------------------------------------------
ffmpeg -y -i saver_loop.mp4 -i spender.mp4 -i "$MUSIC_BED" \
  -filter_complex "[0:v]crop=iw*0.55:ih:iw*0.22:0,scale=540:1920[l]; \
                   [1:v]crop=iw*0.55:ih:iw*0.28:0,scale=540:1920[r]; \
                   [l][r]hstack=inputs=2,format=yuv420p[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 19 -g 30 -keyint_min 30 \
  -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -shortest -t "$OUT_DURATION" \
  public/input-video.mp4

rm -f saver.mp4 saver_loop.mp4 spender.mp4
echo "wrote public/input-video.mp4 (${OUT_DURATION}s)"
