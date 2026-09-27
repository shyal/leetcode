function largestCount(words: string[]): number {
  const count = new Map<string, number>();
  for (const w of words) count.set(w, (count.get(w) ?? 0) + 1);
  let best = 0;
  for (const c of count.values()) {
    if (c > best) best = c;
  }
  return best;
}
