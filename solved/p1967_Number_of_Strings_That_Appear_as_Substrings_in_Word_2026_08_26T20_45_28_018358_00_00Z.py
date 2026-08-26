"""
URL: https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/description/?envType=problem-list-v2&envId=vn57k9wr

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
- "a" appears as a substring in "aaaaabbbbb".
- "b" appears as a substring in "aaaaabbbbb".
- "c" does not appear as a substring in "aaaaabbbbb".
2 of the strings in patterns appear as a substring in word.

Example 3:

Input: patterns = ["a","a","a"], word = "ab"
Output: 3
Explanation:
Each of the patterns appears as a substring in word "ab".

Constraints:

    1 <= patterns.length <= 100
    1 <= patterns[i].length <= 100
    1 <= word.length <= 100
    patterns[i] and word consist of lowercase English letters.
"""


class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        return sum(x in word for x in patterns)


sol = Solution()

print(sol.numOfStrings(["a", "abc", "bc", "d"], "abc"))  # 3

assert sol.numOfStrings(["a", "abc", "bc", "d"], "abc") == 3
assert sol.numOfStrings(["a", "b", "c"], "aaaaabbbbb") == 2
assert sol.numOfStrings(["a", "a", "a"], "ab") == 3

assert sol.numOfStrings([""], "abc") == 1
assert sol.numOfStrings(["a" * 100], "a" * 100) == 1
assert sol.numOfStrings(["z" * 100], "a" * 100) == 0
assert sol.numOfStrings(["abc", "def", "ghi"], "") == 0
assert sol.numOfStrings(["a", "b", "c"], "abcabcabcabcabcabcabcabcabcabc") == 3
assert sol.numOfStrings(["abc", "abc", "abc"], "abc") == 3
assert sol.numOfStrings(["a" * 50, "b" * 50], "a" * 50 + "b" * 50) == 2
assert sol.numOfStrings(["xyz", "yzx", "zxy"], "xyzxyzxyzxyzxyzxyzxyzxyzxyzxyz") == 3
assert sol.numOfStrings(["a", "aa", "aaa", "aaaa"], "aaaaa") == 4
assert sol.numOfStrings(["a" * 100] * 100, "a" * 100) == 100
assert sol.numOfStrings(["a" * 100] * 100, "b" * 100) == 0
assert (
    sol.numOfStrings(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], "abcdefghij")
    == 10
)
