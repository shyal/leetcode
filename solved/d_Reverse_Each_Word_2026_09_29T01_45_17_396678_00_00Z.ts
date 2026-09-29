// DRILL: Reverse Each Word
// TRAINS: ts-string-build
//
// Given a string `s` of words separated by single spaces, return the string
// with every word reversed and the word order kept.
//
// Example 1:
//
// Input: s = "ab cd"
// Output: "ba dc"
//
// Example 2:
//
// Input: s = "x"
// Output: "x"
//
// Example 3:
//
// Input: s = "one two three"
// Output: "eno owt eerht"
//
// Constraints:
//
//     1 <= s.length <= 10^4
//     s has no leading, trailing or double spaces.
//
//     REQUIRED: O(n) with split, map and join; strings are immutable, so
//     each word is turned into an array and back. NO index loop over
//     characters.
// ---
// learning

import assert from "node:assert/strict";

function reverseEachWord(s: string): string {
  return s
    .split(" ")
    .map((w) => w.split("").reverse().join(""))
    .join(" ");
}

console.log(reverseEachWord("one two three"));

assert.deepEqual(reverseEachWord("ab cd"), "ba dc");
assert.deepEqual(reverseEachWord("x"), "x");
assert.deepEqual(reverseEachWord("one two three"), "eno owt eerht");
assert.deepEqual(reverseEachWord("abc"), "cba");
