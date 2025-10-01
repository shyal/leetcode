"""
URL: https://leetcode.com/problems/longest-common-prefix/description/

14. Longest Common Prefix

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".


Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"

Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.


Constraints:

    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] consists of only lowercase English letters if it is non-empty.
"""


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        return "".join(
            x[0]
            for x in takewhile(
                lambda x: all([a == b for a, b in pairwise(x)]), zip(*strs)
            )
        )


sol = Solution()
assert sol.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
assert sol.longestCommonPrefix(["dog", "racecar", "car"]) == ""
assert sol.longestCommonPrefix(["aa", "aaa", "aab"]) == "aa"


