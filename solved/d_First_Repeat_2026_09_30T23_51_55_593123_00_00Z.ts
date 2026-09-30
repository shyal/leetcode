// DRILL: First Repeat
// TRAINS: ts-set-membership
//
// Given an array of numbers `nums`, return the first element equal to an
// earlier element. Return -1 when every element is distinct.
//
// Example 1:
//
// Input: nums = [5, 5]
// Output: 5
//
// Example 2:
//
// Input: nums = [3, 4, 4, 3]
// Output: 4
// Explanation: The second 4 comes before the second 3.
//
// Example 3:
//
// Input: nums = [1, 2, 3]
// Output: -1
//
// Constraints:
//
//     0 <= nums.length <= 10^4
//     0 <= nums[i] <= 10^6
//
//     REQUIRED: O(n): one pass with a Set<number>, has before add. NO
//     indexOf, NO nested loop.

import assert from "node:assert/strict";

function firstRepeat(nums: number[]): number {
  const set = new Set<number>();
  for (const n of nums) {
    if (set.has(n)) return n;
    set.add(n);
  }
  return -1;
}

console.log(firstRepeat([3, 4, 4, 3]));

// assert.deepEqual(firstRepeat([5, 5]), 5);
// assert.deepEqual(firstRepeat([3, 4, 4, 3]), 4);
// assert.deepEqual(firstRepeat([1, 2, 3]), -1);
// assert.deepEqual(firstRepeat([2, 1, 2, 1]), 2);
// assert.deepEqual(firstRepeat([]), -1);
