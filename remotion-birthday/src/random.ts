// Deterministic pseudo-random numbers, seeded per-particle.
//
// Remotion renders can run as many separate processes over different frame
// ranges (this project renders in checkpointed chunks specifically so a
// container restart only loses the current chunk — see the render script).
// Math.random() would make each particle look different every time that
// frame happens to be re-rendered, which shows up as flicker at chunk
// boundaries. mulberry32 is a tiny seeded PRNG: same seed in, same sequence
// out, in any process, forever.
export function mulberry32(seed: number): () => number {
  let a = seed;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** A stable pseudo-random float in [min, max) for a given integer seed. */
export function seededRange(seed: number, min: number, max: number): number {
  const r = mulberry32(seed)();
  return min + r * (max - min);
}
