function positiveTotal(nums: number[]): number {
  let total = 0;
  for (const x of nums) {
    if (x > 0) total += x;
  }
  return total;
}
