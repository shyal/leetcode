"""
URL: https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/description/

1967. Number of Strings That Appear as Substrings in Word

Given an array of strings patterns and a string word, return the number of strings in patterns that exist as a substring in word.

A substring is a contiguous sequence of characters within a string.

Example 1:

Input: patterns = ["a","abc","bc","d"], word = "abc"
Output: 3
Explanation:
- "a" appears as a substring in "abc".
- "abc" appears as a substring in "abc".
- "bc" appears as a substring in "abc".
- "d" does not appear as a substring in "abc".
3 of the strings in patterns appear as a substring in word.

Example 2:

Input: patterns = ["a","b","c"], word = "aaaaabbbbb"
Output: 2
Explanation:
- "a" appears several times.
- "b" appears several times.
- "c" does not appear.
So 2.

Constraints:

    1 <= patterns.length <= 100
    1 <= patterns[i].length <= 100
    1 <= word.length <= 100
    patterns[i] and word consist of lowercase English letters.
"""


class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        res = 0
        for pattern in patterns:
            res += pattern in word
        return res


sol = Solution()

# print(sol.numOfStrings(["a", "abc", "bc", "d"], "abc"))  # 3

assert sol.numOfStrings(["a", "abc", "bc", "d"], "abc") == 3
assert sol.numOfStrings(["a", "b", "c"], "aaaaabbbbb") == 2
assert sol.numOfStrings(["ab"], "a") == 0
assert sol.numOfStrings(["a"], "a") == 1
assert sol.numOfStrings(["a", "a"], "a") == 2
assert sol.numOfStrings(["abc"], "abc") == 1
assert sol.numOfStrings(["aa", "aaa"], "aaaa") == 2
assert sol.numOfStrings(["x"], "abc") == 0
assert sol.numOfStrings(["x", "y", "z"], "abc") == 0
assert sol.numOfStrings(["a", "b", "c"], "abc") == 3
assert sol.numOfStrings(["abc", "def"], "abcdef") == 2
assert sol.numOfStrings(["a", "bc", "def"], "abc") == 2
assert sol.numOfStrings(["zzzz"], "zzz") == 0
assert sol.numOfStrings(["z", "zz", "zzz"], "zzzzz") == 3
