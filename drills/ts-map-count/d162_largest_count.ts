// DRILL: Largest Count
// TRAINS: ts-map-count
//
// Given a non-empty array of strings `words`, return the number of times the
// most frequent word appears.
//
// Example 1:
//
// Input: words = ["a", "b", "a"]
// Output: 2
//
// Example 2:
//
// Input: words = ["x"]
// Output: 1
//
// Example 3:
//
// Input: words = ["p", "q", "q", "q", "r", "r"]
// Output: 3
//
// Constraints:
//
//     1 <= words.length <= 10^4
//     1 <= words[i].length <= 20
//
//     REQUIRED: O(n): one pass counting into a Map<string, number>, then the
//     largest value. NO object literal as the dictionary, NO sort.

import assert from "node:assert/strict";

function largestCount(words: string[]): number {
  throw new Error("not implemented");
}

console.log(largestCount(["a", "b", "a"]));

// assert.deepEqual(largestCount(["a", "b", "a"]), 2);
// assert.deepEqual(largestCount(["x"]), 1);
// assert.deepEqual(largestCount(["p", "q", "q", "q", "r", "r"]), 3);
// assert.deepEqual(largestCount(["m", "n", "n", "m", "m"]), 3);
