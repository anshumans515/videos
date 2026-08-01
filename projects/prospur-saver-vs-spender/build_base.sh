#!/usr/bin/env bash
# Base clip build for the SAVER vs SPENDER reel (PLAYBOOK.md §7, §8).
#
# The source is ALREADY a stacked top/bottom split-screen at 2160x3240:
#   top half    = Anshuman (blue shirt)  — plans, spends less
#   bottom half = Vedant   (white shirt) — spends first, saves last
#
# Three things this script fixes:
#
# 1. FRAMING. Output is 1080x1548 — the *video block* of a 1080x1920 Reel,
#    not the whole canvas. The composition draws a compliance strip and a
#    brand/CTA band underneath it. That is deliberate: the props that carry
#    the story (parcels bottom-left, snacks along the desk, the SAVINGS jar
#    bottom-right) all live low in frame, so a strip floated over the
#    footage would cover the payoff. Bands below the video keep it clear.
#    Cropping vertically rather than horizontally keeps the FULL source
#    width — only 72px come off each half (4.4%) — because the story beats
#    are spread horizontally.
#
# 2. THE SWAP. At the last scene cut (20.4333s) the source swaps the two
#    halves — Vedant moves to the top. Persistent SAVER/SPENDER labels
#    would then be lying, so the final segment is re-stacked in reverse to
#    keep Anshuman on top for the whole reel (character consistency, §8).
#
# 3. AUDIO. Source is ambient-only and very quiet (-29.5 LUFS integrated,
#    -10.8 dBFS peak). Repaired toward the Instagram target with the §7
#    chain. Drop a licensed music_bed.m4a next to this script to use music
#    instead of the room tone.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${1:?path to the source mp4}"

SWAP_AT=20.4333          # last scene cut, where the source swaps the halves
DUR=25.2667
HALF_CROP_H=1548         # of each 1620px source half -> 36px off top and bottom
HALF_CROP_Y=36
OUT_HALF_H=774           # 1080x774 per half -> 1080x1548 stacked

cd "$HERE"
mkdir -p public

# ---------------------------------------------------------------- audio ----
# No speech to protect, so denoise can run harder than the §7 default.
ffmpeg -y -v error -i "$SRC" -map 0:a:0 \
  -af "highpass=f=85,afftdn=nr=18:nf=-32,deesser=i=0.3,acompressor=threshold=-18dB:ratio=3:attack=8:release=180:makeup=1.5,loudnorm=I=-14:TP=-1.5:LRA=11" \
  -ar 48000 -ac 2 fixed.wav

# Two-pass loudness lock (§7). TP aims at -2.0 rather than -1.5 because the
# AAC encode downstream pushes peaks back up ~0.5 dB; aiming at -1.5 here
# lands the finished file at -1.3 dBFS, over the target.
ffmpeg -y -v error -i fixed.wav -af "loudnorm=I=-14:TP=-2.0:LRA=11" -ar 48000 -ac 2 final.wav

if [ -f music_bed.m4a ]; then
  echo "music_bed.m4a found — using it as the audio track"
  ffmpeg -y -v error -i music_bed.m4a -af "loudnorm=I=-14:TP=-2.0:LRA=11" \
    -ar 48000 -ac 2 -t "$DUR" final.wav
fi

# ---------------------------------------------------------------- video ----
# [a] before the swap: crop each half, stack in source order (Anshuman top)
# [b] after  the swap: crop each half, stack REVERSED (Anshuman back on top)
ffmpeg -y -v error -i "$SRC" -i final.wav -filter_complex "
  [0:v]trim=0:${SWAP_AT},setpts=PTS-STARTPTS,split=2[a0][a1];
  [a0]crop=2160:${HALF_CROP_H}:0:${HALF_CROP_Y}[atop];
  [a1]crop=2160:${HALF_CROP_H}:0:$((1620 + HALF_CROP_Y))[abot];
  [atop][abot]vstack=inputs=2[a];

  [0:v]trim=${SWAP_AT},setpts=PTS-STARTPTS,split=2[b0][b1];
  [b0]crop=2160:${HALF_CROP_H}:0:$((1620 + HALF_CROP_Y))[btop];
  [b1]crop=2160:${HALF_CROP_H}:0:${HALF_CROP_Y}[bbot];
  [btop][bbot]vstack=inputs=2[b];

  [a][b]concat=n=2:v=1[cat];
  [cat]scale=1080:$((OUT_HALF_H * 2)):flags=lanczos,
       eq=brightness=0.045:contrast=1.045:saturation=1.06:gamma=1.05,
       format=yuv420p[v]" \
  -map "[v]" -map 1:a:0 \
  -c:v libx264 -preset slow -crf 19 -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 192k -r 30 -t "$DUR" \
  public/input-video.mp4

rm -f fixed.wav
echo "--- built public/input-video.mp4 ---"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration \
  -of default=noprint_wrappers=1 public/input-video.mp4
echo "--- loudness (want I ~ -14, Peak <= -1.5) ---"
ffmpeg -nostats -i public/input-video.mp4 -af ebur128=peak=true -f null - 2>&1 \
  | grep -E "^ +(I|Peak):"
