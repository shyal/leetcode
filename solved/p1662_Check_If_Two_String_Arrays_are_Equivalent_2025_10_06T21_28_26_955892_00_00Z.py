"""
URL: https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/description/

1662. Check If Two String Arrays are Equivalent

Given two string arrays word1 and word2, return true if the two arrays represent the same string, and false otherwise.

A string is represented by an array if the array elements concatenated in order forms the string.

Example 1:

Input: word1 = ["ab", "c"], word2 = ["a", "bc"]
Output: true
Explanation:
word1 represents string "ab" + "c" -> "abc"
word2 represents string "a" + "bc" -> "abc"
Two strings are the same, so return true.

Example 2:

Input: word1 = ["a", "cb"], word2 = ["ab", "c"]
Output: false
Explanation:
word1 represents string "a" + "cb" -> "acb"
word2 represents string "ab" + "c" -> "abc"
They are not the same, so return false.

Example 3:

Input: word1  = ["abc", "d", "defg"], word2 = ["abcddefg"]
Output: true

Constraints:

    1 <= word1.length, word2.length <= 10^3
    1 <= word1[i].length, word2[i].length <= 10^3
    1 <= sum(word1[i].length), sum(word2[i].length) <= 10^3
    word1[i] and word2[i] consist of lowercase letters.
"""


class Solution:
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        return all(a == b for a, b in zip_longest(chain(*word1), chain(*word2)))


sol = Solution()

assert sol.arrayStringsAreEqual(["ab", "c"], ["a", "bc"]) == True
assert sol.arrayStringsAreEqual(["a", "cb"], ["ab", "c"]) == False
assert sol.arrayStringsAreEqual(["abc", "d", "defg"], ["abcddefg"]) == True
assert sol.arrayStringsAreEqual(["a"], ["a"]) == True
assert sol.arrayStringsAreEqual(["a"], ["b"]) == False
assert sol.arrayStringsAreEqual(["ab"], ["a", "b"]) == True
assert sol.arrayStringsAreEqual(["abc"], ["a", "b", "c"]) == True
assert sol.arrayStringsAreEqual(["abc"], ["a", "b", "d"]) == False
assert sol.arrayStringsAreEqual(["a", "b", "c"], ["ab", "c"]) == True
assert sol.arrayStringsAreEqual(["a", "b"], ["a", "c"]) == False
assert sol.arrayStringsAreEqual(["abcd"], ["a", "b", "c", "d"]) == True
assert sol.arrayStringsAreEqual(["aa", "bb"], ["a", "ab", "b"]) == True
assert sol.arrayStringsAreEqual(["aa", "bb"], ["a", "a", "b", "b"]) == True
assert sol.arrayStringsAreEqual(["aa", "bb"], ["a", "a", "b", "c"]) == False
assert sol.arrayStringsAreEqual(["a"], ["ab"]) == False
assert sol.arrayStringsAreEqual(["ab"], ["a"]) == False
