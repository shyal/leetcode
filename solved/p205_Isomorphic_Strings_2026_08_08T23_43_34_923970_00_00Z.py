"""
URL: https://leetcode.com/problems/isomorphic-strings/description/?envType=problem-list-v2&envId=vn57k9wr

205. Isomorphic Strings

Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while
preserving the order of characters. No two characters may map to the same
character, but a character may map to itself.


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
The strings s and t can not be made identical as '1' needs to be mapped to
both '2' and '3'.

Example 3:

Input: s = "paper", t = "title"
Output: true


Constraints:

    1 <= s.length <= 5 * 10^4
    t.length == s.length
    s and t consist of any valid ascii character.
"""


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        return [s.index(x) for x in s] == [t.index(x) for x in t]


sol = Solution()

# print(sol.isIsomorphic("egg", "add"))  # True

assert sol.isIsomorphic("egg", "add") == True
assert sol.isIsomorphic("f11", "b23") == False
assert sol.isIsomorphic("paper", "title") == True
assert sol.isIsomorphic("foo", "bar") == False
assert sol.isIsomorphic("a", "a") == True
assert sol.isIsomorphic("a", "b") == True
assert sol.isIsomorphic("ab", "aa") == False
assert sol.isIsomorphic("aa", "ab") == False
assert sol.isIsomorphic("abab", "baba") == True
assert sol.isIsomorphic("badc", "baba") == False
assert sol.isIsomorphic("abc", "ddd") == False
assert sol.isIsomorphic("ddd", "abc") == False
assert sol.isIsomorphic("aaaa", "aaab") == False
assert sol.isIsomorphic("aaab", "aaaa") == False
assert sol.isIsomorphic("abcd", "wxyz") == True
assert sol.isIsomorphic("Aa", "aa") == False
assert sol.isIsomorphic("Aa", "bc") == True
assert sol.isIsomorphic("!@!", "aba") == True
assert sol.isIsomorphic("!@!", "abc") == False
assert sol.isIsomorphic("a1a1", "b2b2") == True
assert sol.isIsomorphic("a b", "c d") == True
assert sol.isIsomorphic("a b", "cdd") == False
assert sol.isIsomorphic("13579", "24680") == True
assert sol.isIsomorphic("turtle", "tletur") == True
assert sol.isIsomorphic("ab" * 25000, "cd" * 25000) == True
assert sol.isIsomorphic("a" * 49999 + "b", "a" * 50000) == False