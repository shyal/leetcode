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

Solved. Passes on leetcode.

"""


class Solution:
    def counts_match(self, test, target):
        for key in target:
            if key not in test:
                return False
            if test[key] < target[key]:
                return False
        return bool(target)

    def minWindow(self, s: str, t: str) -> str:
        left = 0
        best = float("inf")
        best_str = ""
        count = defaultdict(int)
        tcount = dict(Counter(t))
        for right, c in enumerate(s):
            count[c] += 1
            while self.counts_match(count, tcount):
                if right - left + 1 < best:
                    best_str = s[left : right + 1]
                    best = right - left + 1
                count[s[left]] -= 1
                if count[s[left]] == 0:
                    del count[s[left]]
                left += 1
        return best_str


sol = Solution()


assert sol.counts_match({"a": 1}, {"a": 1}) == True
assert sol.counts_match({"a": 1}, {"2": 1}) == False
assert sol.counts_match({"a": 1, "b": 2}, {"a": 1}) == True
assert sol.counts_match({"a": 5, "b": 2}, {"a": 1}) == True

assert sol.minWindow("a", "") == ""

print(sol.minWindow("ADOBECODEBANC", "ABC"))  # "BANC"

assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
assert sol.minWindow("a", "a") == "a"
assert sol.minWindow("a", "aa") == ""

assert sol.minWindow("", "a") == ""
assert sol.minWindow("a" * 99999 + "b", "ab") == "ab"
assert sol.minWindow("b" + "a" * 99999, "ab") == "ba"
assert sol.minWindow("abcde" * 20000, "edcba") == "abcde"
assert sol.minWindow("aabbcc", "abc") == "abbc"
assert sol.minWindow("aabbcc", "aabbcc") == "aabbcc"
assert sol.minWindow("aabbcc", "aaabbbccc") == ""
assert sol.minWindow("xyz", "a") == ""
assert sol.minWindow("a" * 50000 + "b" * 50000, "ab") == "ab"
assert sol.minWindow("a" * 50000 + "b" * 50000, "ba") == "ab"
