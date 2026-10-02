"""
URL: https://leetcode.com/problems/isomorphic-strings/description/?envType=problem-list-v2&envId=vn57k9wr

205. Isomorphic Strings

Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.

Example 1:

Input: s = "egg", t = "add"
Output: true
Explanation:
The strings s and t can be made identical by:
- Mapping 'e' to 'a'.
- Mapping 'g' to 'd'.

Example 2:

Input: s = "f11", t = "b23"
Output: false
Explanation:
The strings s and t can not be made identical as '1' needs to be mapped to both '2' and '3'.

Example 3:

Input: s = "paper", t = "title"
Output: true

Constraints:

    1 <= s.length <= 5 * 10^4
    t.length == s.length
    s and t consist of any valid ascii character.

---

LEETCODE: Accepted (7 ms, 22.1 MB)
"""


# mu 0.7
# def isIsomorphic(A: str, B: str) -> bool
#   a = {:list}
#   b = {:list}
#   r = {:list}
#   for i, c in A
#     a[c] <- i
#   for i, c in B
#     b[c] <- i
#   for (ka, kb) in zip(a, b)
#     if a[ka] != b[kb]
#       return False
#   return True

from collections import defaultdict


class Solution:
    def isIsomorphic(self, A: str, B: str) -> bool:
        a = defaultdict(list)
        b = defaultdict(list)
        r = defaultdict(list)
        for i, c in enumerate(A):
            a[c].append(i)
        for i, c in enumerate(B):
            b[c].append(i)
        for (ka, kb) in zip(a, b):
            if a[ka] != b[kb]:
                return False
        return True


sol = Solution()
sol.isIsomorphic('abcabc', 'xyzxyz')
print(sol.isIsomorphic('egg', 'add'))
assert sol.isIsomorphic('egg', 'add') is True
assert sol.isIsomorphic('foo', 'bar') is False
assert sol.isIsomorphic('paper', 'title') is True
assert sol.isIsomorphic('', '') == True
assert sol.isIsomorphic('a', 'a') == True
assert sol.isIsomorphic('a', 'b') == True
assert sol.isIsomorphic('abc', 'def') == True
assert sol.isIsomorphic('abc', 'dee') == False
assert sol.isIsomorphic('aaa', 'bbb') == True
assert sol.isIsomorphic('abcabc', 'xyzxyz') == True
assert sol.isIsomorphic('abcabc', 'xyzyxz') == False
assert sol.isIsomorphic('abcdefghijklmnopqrstuvwxyz', 'bcdefghijklmnopqrstuvwxyza') == True
assert sol.isIsomorphic('abcdefghijklmnopqrstuvwxyz' * 2000, 'bcdefghijklmnopqrstuvwxyza' * 2000) == True
assert sol.isIsomorphic('12345', '54321') == True
assert sol.isIsomorphic('!@#$%', '%$#@!') == True
