"""
URL: https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/description/

28. Find the Index of the First Occurrence in a String

Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.


Example 1:

Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.

Example 2:

Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.


Constraints:

    1 <= haystack.length, needle.length <= 104
    haystack and needle consist of only lowercase English characters.
"""


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        for i in range(len(haystack) - len(needle) + 1):
            all_match = True
            for j in range(len(needle)):
                if haystack[i + j] != needle[j]:
                    all_match = False
                    break
            if all_match:
                return i
        return -1


sol = Solution()
assert sol.strStr("sadbutsad", "sad") == 0
assert sol.strStr("sad", "sad") == 0
assert sol.strStr("leetcode", "leeto") == -1
assert sol.strStr("s", "s") == 0
assert sol.strStr("sa", "s") == 0
assert sol.strStr("0123sa", "sa") == 4


