// DRILL: Positive Total
// TRAINS: ts-typed-function
//
// Given an array of numbers `nums`, return the sum of the elements greater
// than 0. An array with no positive element sums to 0.
//
// Example 1:
//
// Input: nums = [3, -1, 4]
// Output: 7
//
// Example 2:
//
// Input: nums = [-2, -5]
// Output: 0
//
// Example 3:
//
// Input: nums = []
// Output: 0
//
// Constraints:
//
//     0 <= nums.length <= 10^4
//     -10^6 <= nums[i] <= 10^6
//
//     REQUIRED: O(n) with one for..of loop; the parameter and the return
//     value both carry a type annotation. NO any.

import assert from "node:assert/strict";

function positiveTotal(nums: number[]): number {
  let res: number = 0;
  for (const n of nums) {
    if (n > 0) res += n;
  }
  return res;
}

console.log(positiveTotal([3, -1, 4]));

assert.deepEqual(positiveTotal([3, -1, 4]), 7);
assert.deepEqual(positiveTotal([-2, -5]), 0);
assert.deepEqual(positiveTotal([]), 0);
assert.deepEqual(positiveTotal([1, 2, 3, 4, 5]), 15);
