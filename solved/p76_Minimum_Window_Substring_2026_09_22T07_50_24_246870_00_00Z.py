"""
URL: https://leetcode.com/problems/minimum-window-substring/description/?envType=problem-list-v2&envId=vn57k9wr

76. Minimum Window Substring

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Example 1:

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:

Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.

Example 3:

Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

Constraints:

    m == s.length
    n == t.length
    1 <= m, n <= 10^5
    s and t consist of uppercase and lowercase English letters.

Follow up:
Could you find an algorithm that runs in O(m + n) time?

---

LEETCODE: Accepted (731 ms, 19.7 MB)
"""


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        tcount = Multiset(t)
        scount = Multiset()
        res = ""
        left = 0

        def counts_match(a, b):
            for k, v in a.items():
                if b[k] == 0 or b[k] < v:
                    return False
            return bool(t)

        for right, c in enumerate(s):
            scount[c] += 1
            while left <= right and counts_match(tcount, scount):
                sub = s[left : right + 1]
                if res == "" or len(sub) < len(res):
                    res = sub
                scount[s[left]] -= 1
                left += 1

        return res


sol = Solution()

print(sol.minWindow("ADOBECODEBANC", "ABC"))  # "BANC"

assert sol.minWindow("cabwefgewcwaefgcf", "cae") == "cwae"

assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
assert sol.minWindow("a", "a") == "a"
assert sol.minWindow("a", "aa") == ""

assert sol.minWindow("", "a") == ""
assert sol.minWindow("a", "") == ""
assert sol.minWindow("a" * 99999 + "b", "ab") == "ab"
assert sol.minWindow("b" + "a" * 99999, "ab") == "ba"
assert sol.minWindow("abcde" * 20000, "edcba") == "abcde"
assert sol.minWindow("aabbcc", "abc") == "abbc"
assert sol.minWindow("aabbcc", "aabbcc") == "aabbcc"
assert sol.minWindow("aabbcc", "aaabbbccc") == ""
assert sol.minWindow("xyz", "a") == ""
assert sol.minWindow("a" * 50000 + "b" * 50000, "ab") == "ab"
assert sol.minWindow("a" * 50000 + "b" * 50000, "ba") == "ab"
