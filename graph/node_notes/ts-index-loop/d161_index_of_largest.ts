function indexOfLargest(nums: number[]): number {
  let best = 0;
  for (let i = 1; i < nums.length; i++) {
    if (nums[i] > nums[best]) best = i;
  }
  return best;
}
