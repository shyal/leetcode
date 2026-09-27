// DRILL: Index Of Largest
// TRAINS: ts-index-loop
//
// Given a non-empty array of numbers `nums`, return the index of its largest
// element. When the largest value appears more than once, return its first
// index.
//
// Example 1:
//
// Input: nums = [9, 2, 5]
// Output: 0
//
// Example 2:
//
// Input: nums = [1, 7, 7]
// Output: 1
//
// Example 3:
//
// Input: nums = [2, 4, 9]
// Output: 2
//
// Constraints:
//
//     1 <= nums.length <= 10^4
//     -10^6 <= nums[i] <= 10^6
//
//     REQUIRED: O(n) with one index loop, for (let i = 0; ...). NO Math.max,
//     NO indexOf.

import assert from "node:assert/strict";

function indexOfLargest(nums: number[]): number {
  let max: number = 0;
  for (let i: number = 0; i < nums.length; i++) {
    if (nums[i] > nums[max]) {
      max = i;
    }
  }
  return max;
}

console.log(indexOfLargest([9, 2, 5]));

assert.deepEqual(indexOfLargest([9, 2, 5]), 0);
assert.deepEqual(indexOfLargest([1, 7, 7]), 1);
assert.deepEqual(indexOfLargest([2, 4, 9]), 2);
assert.deepEqual(indexOfLargest([-3]), 0);
