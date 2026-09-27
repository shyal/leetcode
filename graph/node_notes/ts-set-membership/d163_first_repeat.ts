function firstRepeat(nums: number[]): number {
  const seen = new Set<number>();
  for (const x of nums) {
    if (seen.has(x)) return x;
    seen.add(x);
  }
  return -1;
}
