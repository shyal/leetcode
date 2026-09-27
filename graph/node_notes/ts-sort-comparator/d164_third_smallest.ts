function thirdSmallest(nums: number[]): number {
  const sorted = [...nums].sort((a, b) => a - b);
  return sorted[2];
}
