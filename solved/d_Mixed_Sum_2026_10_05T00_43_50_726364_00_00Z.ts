// DRILL: Mixed Sum
// TRAINS: ts-union-narrowing
//
// Given an array `values` whose elements are numbers or strings holding a
// number, return the sum of all of them as a number.
//
// Example 1:
//
// Input: values = ["2", 1, 3]
// Output: 6
//
// Example 2:
//
// Input: values = ["10"]
// Output: 10
//
// Example 3:
//
// Input: values = [4, 5, "6"]
// Output: 15
//
// Constraints:
//
//     0 <= values.length <= 10^4
//     Every string parses as a finite number.
//
//     REQUIRED: O(n); the parameter is typed as an array of a union, and each
//     element is narrowed with typeof before use. NO any, NO as.

import assert from "node:assert/strict";

function mixedSum(values: (number | string)[]): number {
  let res: number = 0;
  for (const val of values) {
    if (typeof val == "string") {
      res += Number(val);
    } else {
      res += val;
    }
  }
  return res;
}

console.log(mixedSum(["2", 1, 3]));

assert.deepEqual(mixedSum(["2", 1, 3]), 6);
assert.deepEqual(mixedSum(["10"]), 10);
assert.deepEqual(mixedSum([4, 5, "6"]), 15);
assert.deepEqual(mixedSum([]), 0);
assert.deepEqual(mixedSum([1, "2", 3, "4", 5]), 15);
