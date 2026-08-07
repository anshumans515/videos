#!/usr/bin/env bash
# Checkpointed render: the full 23,920-frame timeline in ~3000-frame chunks
# (~9-10 min each at this sandbox's measured ~5.3 fps), so a container
# restart loses at most one chunk instead of the whole ~75-minute run — this
# container has already restarted once mid-build today.
#
# Resumable: re-running this script skips any chunk whose output file
# already exists with the expected duration, so it picks up wherever a
# previous run left off.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

CHROME=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell  # this sandbox only
TOTAL_FRAMES=23920
CHUNK=3000
FPS=30
OUT_DIR="$HERE/chunks"
FINAL="$HERE/out/birthday-final.mp4"

mkdir -p "$OUT_DIR" "$HERE/out"

chunk_ok() {
  local f="$1" expect_frames="$2"
  [ -s "$f" ] || return 1
  local dur
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null || echo 0)
  local expect_dur
  expect_dur=$(awk "BEGIN{print $expect_frames/$FPS}")
  # within 0.5s of expected — a chunk that's short/zero means a previous run
  # died mid-encode; anything else close enough is a completed chunk.
  awk -v d="$dur" -v e="$expect_dur" 'BEGIN{exit !(d > e-0.5)}'
}

start=0
i=0
CHUNK_LIST=()
while [ "$start" -lt "$TOTAL_FRAMES" ]; do
  end=$((start + CHUNK - 1))
  if [ "$end" -ge "$TOTAL_FRAMES" ]; then
    end=$((TOTAL_FRAMES - 1))
  fi
  n=$(printf "%02d" "$i")
  out="$OUT_DIR/chunk_${n}.mp4"
  frames=$((end - start + 1))

  if chunk_ok "$out" "$frames"; then
    echo "[chunk $n] $start-$end already rendered ($frames frames) — skipping"
  else
    echo "[chunk $n] rendering frames $start-$end ($frames frames)..."
    npx remotion render BirthdayReel "$out" --browser-executable="$CHROME" \
      --frames="${start}-${end}" 2>&1 | grep -viE "memory|cgroup|meminfo|docker|differing"
    echo "[chunk $n] done"
  fi

  CHUNK_LIST+=("$out")
  start=$((end + 1))
  i=$((i + 1))
done

echo "--- all ${#CHUNK_LIST[@]} chunks present, concatenating ---"
: > "$OUT_DIR/concat.txt"
for f in "${CHUNK_LIST[@]}"; do
  echo "file '$f'" >> "$OUT_DIR/concat.txt"
done

ffmpeg -y -v error -f concat -safe 0 -i "$OUT_DIR/concat.txt" -c copy "$FINAL"

echo "--- final ---"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$FINAL"
echo "expected duration: $(awk "BEGIN{print $TOTAL_FRAMES/$FPS}")s"
echo "RENDER_CHUNKS_COMPLETE"
