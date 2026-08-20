"""
URL: https://leetcode.com/problems/minimum-window-substring/description/?envType=problem-list-v2&envId=vn57k9wr

76. Minimum Window Substring

Given two strings s and t of lengths m and n respectively, return the minimum
window substring of s such that every character in t (including duplicates) is
included in the window. If there is no such substring, return the empty string "".

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


Follow up: Could you find an algorithm that runs in O(m + n) time?

---

Brute force passes, and sliding window was close. But i'm wasting time
when i should be building sliding window drills. So i'm marking this
as a fail.

"""


class Solution:
    def minWindowBruteForce(self, s: str, t: str) -> str:
        shortest_window = ""
        tcounter = Counter(t)
        for i in range(len(s)):
            for j in range(i, len(s)):
                ss = s[i : j + 1]
                scounter = Counter(ss)
                t_in_s = False
                for sl in tcounter:
                    if sl not in scounter or scounter[sl] < tcounter[sl]:
                        break
                else:
                    t_in_s = len(s)
                if t_in_s:
                    if not shortest_window:
                        shortest_window = ss
                    else:
                        shortest_window = (
                            ss if len(ss) < len(shortest_window) else shortest_window
                        )
        return shortest_window

    def minWindow(self, s: str, t: str) -> str:
        left = 0
        right = len(t) - 1
        window_counter = Counter(s[left : right + 1])
        target_counter = Counter(t)

        def all_present(window_counter, target_counter):
            t_in_w = False
            for sl in target_counter:
                if sl not in window_counter or window_counter[sl] < target_counter[sl]:
                    break
            else:
                t_in_w = len(s)
            return t_in_w

        print(window_counter)

        min_window = t

        while right <= len(s) - 1:
            ss = s[left : right + 1]
            window_counter = Counter(ss)
            if all_present(window_counter, target_counter):
                min_window = ss if len(ss) < len(min_window) else min_window
                if left <= right - len(t):
                    left += 1
                if left >= len(s) - len(t):
                    break
                continue
            right += 1

        return min_window


sol = Solution()

print(sol.minWindow("ADOBECODEBANC", "ABC"))  # "BANC"

# assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
# assert sol.minWindow("a", "a") == "a"
# assert sol.minWindow("a", "aa") == ""

# assert sol.minWindow("", "a") == ""
# # assert sol.minWindow("a", "") == ""
# assert sol.minWindow("ab", "abc") == ""
# assert sol.minWindow("abc", "d") == ""
# assert sol.minWindow("abc", "abd") == ""
# assert sol.minWindow("ab", "aab") == ""

# assert sol.minWindow("ab", "a") == "a"
# assert sol.minWindow("ab", "b") == "b"
# assert sol.minWindow("ab", "ab") == "ab"
# assert sol.minWindow("ab", "ba") == "ab"
# assert sol.minWindow("abc", "cba") == "abc"
# assert sol.minWindow("bba", "ab") == "ba"
# assert sol.minWindow("baab", "ab") == "ba"
# assert sol.minWindow("abcb", "b") == "b"
# assert sol.minWindow("abcdef", "ba") == "ab"
# assert sol.minWindow("xxxxab", "ab") == "ab"
# assert sol.minWindow("aaab", "ab") == "ab"

# assert sol.minWindow("aa", "aa") == "aa"
# assert sol.minWindow("aaa", "aa") == "aa"
# assert sol.minWindow("aab", "aab") == "aab"
# assert sol.minWindow("abab", "aab") == "aba"

# assert sol.minWindow("Aa", "aA") == "Aa"
# assert sol.minWindow("AaBb", "ab") == "aBb"
# assert sol.minWindow("ADOBECODEBANC", "ABCC") == "CODEBANC"

# assert sol.minWindow("cabwefgewcwaefgcf", "cae") == "cwae"
# assert sol.minWindow("aaaaaaaaaaaabbbbbcdd", "abcdd") == "abbbbbcdd"
# assert sol.minWindow("of_characters_and_as", "aas") == "and_as"


# FAILED: walked away after 45m 8s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
