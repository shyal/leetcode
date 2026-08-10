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

---
e -> 0
g -> 1,2

a -> 0
d -> 1,2

So build a dict, with keys are letters, and positions as a list of ints, for both words, then verify that the values match
"""



class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        sd, td = defaultdict(list), defaultdict(list)
        [sd[v].append(i) for i, v in enumerate(s)]
        [td[v].append(i) for i, v in enumerate(t)]
        return [*sd.values()] == [*td.values()]


sol = Solution()

# print(sol.isIsomorphic("egg", "add"))  # True

assert sol.isIsomorphic("egg", "add") is True
assert sol.isIsomorphic("foo", "bar") is False
assert sol.isIsomorphic("paper", "title") is True
assert sol.isIsomorphic("f11", "b23") is False

assert sol.isIsomorphic("", "") is True
assert sol.isIsomorphic("a", "a") is True
assert sol.isIsomorphic("a", "b") is True

assert sol.isIsomorphic("ab", "abc") is False
assert sol.isIsomorphic("abc", "ab") is False
assert sol.isIsomorphic("a", "") is False
assert sol.isIsomorphic("", "a") is False

assert sol.isIsomorphic("ab", "aa") is False
assert sol.isIsomorphic("aa", "ab") is False
assert sol.isIsomorphic("aa", "bb") is True
assert sol.isIsomorphic("abc", "xxy") is False
assert sol.isIsomorphic("aab", "xxy") is True

assert sol.isIsomorphic("abab", "baba") is True
assert sol.isIsomorphic("aba", "baa") is False
assert sol.isIsomorphic("abba", "cddc") is True
assert sol.isIsomorphic("abba", "cddd") is False
assert sol.isIsomorphic("badc", "baba") is False
assert sol.isIsomorphic("abcabc", "xyzxyz") is True

assert sol.isIsomorphic("Aa", "bB") is True
assert sol.isIsomorphic("aA", "bb") is False
assert sol.isIsomorphic("a b", "c d") is True
assert sol.isIsomorphic("  ", "ab") is False
assert sol.isIsomorphic("!@#", "$%^") is True
assert sol.isIsomorphic("13", "42") is True

assert sol.isIsomorphic("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz") is True
assert sol.isIsomorphic("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba") is True
assert sol.isIsomorphic("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxya") is False

assert sol.isIsomorphic("ab" * 25000, "cd" * 25000) is True
assert sol.isIsomorphic("ab" * 25000, "cc" * 25000) is False
assert sol.isIsomorphic("a" * 50000, "b" * 50000) is True
assert sol.isIsomorphic("a" * 49999 + "b", "c" * 49999 + "c") is False

_ascii = "".join(chr(i) for i in range(128))
assert sol.isIsomorphic(_ascii, _ascii[::-1]) is True
assert sol.isIsomorphic(_ascii, "x" * 128) is False