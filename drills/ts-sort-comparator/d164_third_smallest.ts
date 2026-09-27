// DRILL: Third Smallest
// TRAINS: ts-sort-comparator
//
// Given an array of at least three numbers `nums`, return its third smallest
// element, counting repeats. The array `nums` must be the same after the call.
//
// Example 1:
//
// Input: nums = [10, 9, 100]
// Output: 100
//
// Example 2:
//
// Input: nums = [3, 1, 2]
// Output: 3
//
// Example 3:
//
// Input: nums = [5, 5, 1, 7]
// Output: 5
//
// Constraints:
//
//     3 <= nums.length <= 10^4
//     0 <= nums[i] <= 10^6
//
//     REQUIRED: sort a copy with a numeric comparator, O(n log n). The input
//     array must NOT change. NO sort without a comparator.

import assert from "node:assert/strict";

function thirdSmallest(nums: number[]): number {
  throw new Error("not implemented");
}

console.log(thirdSmallest([10, 9, 100]));

// assert.deepEqual(thirdSmallest([10, 9, 100]), 100);
// assert.deepEqual(thirdSmallest([3, 1, 2]), 3);
// assert.deepEqual(thirdSmallest([5, 5, 1, 7]), 5);
// assert.deepEqual(thirdSmallest([20, 3, 15, 8, 1]), 8);
// const nums = [3, 1, 2];
// thirdSmallest(nums);
// assert.deepEqual(nums, [3, 1, 2]);
