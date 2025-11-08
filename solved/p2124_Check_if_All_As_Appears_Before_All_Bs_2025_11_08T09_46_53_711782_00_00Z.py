"""
URL: https://leetcode.com/problems/check-if-all-as-appears-before-all-bs/description/?envType=problem-list-v2&envId=vn57k9wr

2124. Check if All A's Appears Before All B's

Given a string s consisting of only the characters 'a' and 'b', return true if every 'a' appears before every 'b' in the string. Otherwise, return false.

Example 1:

Input: s = "aaabbb"
Output: true
Explanation:
The 'a's are at indices 0, 1, and 2, while the 'b's are at indices 3, 4, and 5.
Hence, every 'a' appears before every 'b' and we return true.

Example 2:

Input: s = "abab"
Output: false
Explanation:
There is an 'a' at index 2 and a 'b' at index 1.
Hence, not every 'a' appears before every 'b' and we return false.

Example 3:

Input: s = "bbb"
Output: true
Explanation:
There are no 'a's, hence, every 'a' appears before every 'b' and we return true.

Constraints:

    1 <= s.length <= 100
    s[i] is either 'a' or 'b'.
"""


class Solution:
    def checkString(self, s: str) -> bool:
        res = [[a, "".join(b)] for a, b in groupby(s, key=lambda x: x)]
        if len(res) == 1:
            return True
        elif len(res) == 2:
            return next(iter(next(iter(res), [])), "") == "a"
        return False


sol = Solution()

# print(sol.checkString("aaabbba"))  # true

assert sol.checkString("aaabbb") == True
assert sol.checkString("abab") == False
assert sol.checkString("bbb") == True
assert sol.checkString("a") == True
assert sol.checkString("b") == True
assert sol.checkString("ab") == True
assert sol.checkString("ba") == False
assert sol.checkString("aa") == True
assert sol.checkString("bb") == True
assert sol.checkString("aba") == False
assert sol.checkString("bbba") == False
assert sol.checkString("aaab") == True
assert sol.checkString("baa") == False
assert sol.checkString("ababab") == False
assert sol.checkString("aaaaabbbbb") == True
assert sol.checkString("bbbbbaaaaa") == False
assert sol.checkString("aabb") == True
assert sol.checkString("bbaa") == False
assert sol.checkString("ababba") == False
assert sol.checkString("aaabbba") == False
