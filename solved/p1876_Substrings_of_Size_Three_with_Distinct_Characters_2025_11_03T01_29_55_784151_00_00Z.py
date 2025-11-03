"""
URL: https://leetcode.com/problems/substrings-of-size-three-with-distinct-characters/description/?envType=problem-list-v2&envId=vn57k9wr

1876. Substrings of Size Three with Distinct Characters

A string is good if there are no repeated characters.

Given a string s, return the number of good substrings of length three in s.

Note that if there are multiple occurrences of the same substring, every occurrence should be counted.

A substring is a contiguous sequence of characters in a string.

Example 1:

Input: s = "xyzzaz"
Output: 1
Explanation: There are 4 substrings of size 3: "xyz", "yzz", "zza", and "zaz".
The only good substring of length 3 is "xyz".

Example 2:

Input: s = "aababcabc"
Output: 4
Explanation: There are 7 substrings of size 3: "aab", "aba", "bab", "abc", "bca", "cab", and "abc".
The good substrings are "abc", "bca", "cab", and "abc".

Constraints:

    1 <= s.length <= 100
    s consists of lowercase English letters.
"""


class Solution:
    def countGoodSubstrings(self, s: str) -> int:
        return sum(
            len(s[i : i + 3]) == len(set(s[i : i + 3])) for i in range(len(s) - 2)
        )


sol = Solution()

# print(sol.countGoodSubstrings("xyzzaz"))  # 1

assert sol.countGoodSubstrings("xyzzaz") == 1
assert sol.countGoodSubstrings("aababcabc") == 4
assert sol.countGoodSubstrings("a") == 0
assert sol.countGoodSubstrings("ab") == 0
assert sol.countGoodSubstrings("abc") == 1
assert sol.countGoodSubstrings("aaa") == 0
assert sol.countGoodSubstrings("xyx") == 0
assert sol.countGoodSubstrings("abcde") == 3
assert sol.countGoodSubstrings("aabbcc") == 0
assert sol.countGoodSubstrings("abacaba") == 2
assert sol.countGoodSubstrings("abcabc") == 4
assert sol.countGoodSubstrings("aaaaa") == 0
