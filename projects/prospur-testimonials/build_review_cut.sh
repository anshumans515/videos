#!/usr/bin/env bash
# Builds a review copy of the 14-clip merge with each clip's number and
# timecode burned into the corner, so a human compliance reviewer always
# knows which clip they're hearing and can record a verdict against it.
#
# Why this exists: these are customer testimonials for an AMFI-registered
# MFD, so any clip where a speaker states returns/performance/gains cannot
# be published (PLAYBOOK.md §2). Automated transcription is unavailable in
# this environment — every Whisper model host (HuggingFace, Azure, GitHub
# release assets, jsDelivr) is blocked by the network policy, and the one
# recognizer that ships weights offline (pocketsphinx) produces unusable
# output on this accented, phone-recorded speech. So the review is a human
# listen; this just makes it a cheap one.
#
# Deliberately low resolution and bitrate: this is a review artifact, not a
# publishing master. Audio fidelity is what matters for the task, so the
# video budget is spent down to keep the file small enough to watch on a
# phone / send over chat.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/public/testimonials-merged.mp4"
OUT="$HERE/public/testimonials-review.mp4"

[ -f "$SRC" ] || { echo "missing $SRC — run ./build_merge.sh first" >&2; exit 1; }

# clip:start:end — matches the running order in build_merge.sh exactly.
CLIPS="
01:0:70.13
02:70.13:128.23
03:128.23:142.83
04:142.83:177.34
05:177.34:239.24
06:239.24:273.14
07:273.14:359.24
08:359.24:406.64
09:406.64:452.98
10:452.98:491.81
11:491.81:596.91
12:596.91:645.84
13:645.84:724.64
14:724.64:794.04
"

fmt_tc() { awk -v s="$1" 'BEGIN{printf "%d:%02d", int(s/60), int(s%60)}'; }

FILTER="scale=480:-2"
while IFS=: read -r n start end; do
  [ -z "${n:-}" ] && continue
  label="CLIP ${n}   $(fmt_tc "$start")-$(fmt_tc "$end")"
  # Escape the colons in the timecode. drawtext parses ':' as its own option
  # separator even inside a quoted text= value, so an unescaped "1:10" makes
  # ffmpeg read the remainder as a new option and die with the misleading
  # "Both text and text file provided".
  label=$(printf '%s' "$label" | sed 's/:/\\:/g')
  FILTER="${FILTER},drawtext=text='${label}':x=12:y=12:fontsize=17:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=6:enable='between(t\,${start}\,${end})'"
done <<< "$CLIPS"

echo "encoding review cut (low bitrate, labels burned in)..."
ffmpeg -y -v error -i "$SRC" -vf "$FILTER" \
  -c:v libx264 -preset medium -crf 33 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 80k -ar 44100 "$OUT"

echo "--- review cut ---"
ls -la "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
