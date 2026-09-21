"""
URL: https://leetcode.com/problems/reorganize-string/description/?envType=problem-list-v2&envId=vn57k9wr

767. Reorganize String

Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.

Return any possible rearrangement of s or return "" if not possible.

Example 1:

Input: s = "aab"
Output: "aba"

Example 2:

Input: s = "aaab"
Output: ""

Constraints:

    1 <= s.length <= 500
    s consists of lowercase English letters.

---

LEETCODE: Accepted (5 ms, 19.6 MB)
"""


class Solution:
    def reorganizeString(self, s: str) -> str:
        h = [[v, k] for k, v in Counter(s).items()]
        maxheapify(h)
        res = ""
        keep = []
        while h:
            count, letter = maxheappop(h)
            res += letter
            if keep:
                maxheappush(h, keep.pop())
            if count - 1 > 0:
                keep.append([count - 1, letter])
        return res if not keep else ""


sol = Solution()

print(sol.reorganizeString("aab"))  # "aba" or "bab"
print(sol.reorganizeString("aaab"))
print(sol.reorganizeString("aaabbbccc"))
print(sol.reorganizeString("aaaabbcc"))

# assert sol.reorganizeString("aab") in ["aba", "bab"]
# assert sol.reorganizeString("aaab") == ""

# assert sol.reorganizeString("a") == "a"
# assert sol.reorganizeString("aa") == ""
# assert sol.reorganizeString("abc") == "abc"
# assert sol.reorganizeString("aabbcc") == "abcabc"
# assert sol.reorganizeString("aaaabbcc") == "abacabac"
# assert sol.reorganizeString("aaabbbccc") == "abcabcabc"
