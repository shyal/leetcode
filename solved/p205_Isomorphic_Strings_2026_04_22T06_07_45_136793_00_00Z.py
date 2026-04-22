"""
URL: https://leetcode.com/problems/isomorphic-strings/description/?envType=problem-list-v2&envId=vn57k9wr

205. Isomorphic Strings

Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving
the order of characters. No two characters may map to the same character, but a character
may map to itself.


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

Input: s = "paper", t = "title"

p -> 0, 2
a -> 1
e -> 3
r -> 4

t -> 0, 2
i -> 1
l -> 3
e -> 4

"""

class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        def get_pos(s):
            p = defaultdict(list)
            for i, c in enumerate(s):
                p[c].append(i)
            return list(p.values())
        return list(get_pos(s)) == list(get_pos(t))


sol = Solution()

# print(sol.isIsomorphic("egg", "add"))  # True

assert sol.isIsomorphic("egg", "add") == True
assert sol.isIsomorphic("foo", "bar") == False
assert sol.isIsomorphic("paper", "title") == True
assert sol.isIsomorphic("f11", "b23") == False
assert sol.isIsomorphic("a", "a") == True
assert sol.isIsomorphic("a", "b") == True
assert sol.isIsomorphic("ab", "aa") == False
assert sol.isIsomorphic("aa", "ab") == False
assert sol.isIsomorphic("abc", "abc") == True
assert sol.isIsomorphic("abcdef", "ghijkl") == True
assert sol.isIsomorphic("aabb", "ccdd") == True
assert sol.isIsomorphic("abab", "cdcd") == True
assert sol.isIsomorphic("abba", "cddc") == True
assert sol.isIsomorphic("abab", "cddc") == False
assert sol.isIsomorphic("abcabc", "xyzxyz") == True
assert sol.isIsomorphic("abcabd", "xyzxyz") == False
assert sol.isIsomorphic("13", "42") == True
assert sol.isIsomorphic("!@#", "$%^") == True
assert sol.isIsomorphic("a b", "c d") == True
assert sol.isIsomorphic("ab ", "cd ") == True
assert sol.isIsomorphic("ab", "ba") == True
assert sol.isIsomorphic("aba", "bab") == True
assert sol.isIsomorphic("badc", "baba") == False
assert sol.isIsomorphic("a" * 1000, "b" * 1000) == True
assert sol.isIsomorphic("a" * 999 + "b", "c" * 999 + "c") == False
assert sol.isIsomorphic("ab", "cc") == False
assert sol.isIsomorphic("abcdefg", "gfedcba") == True
assert sol.isIsomorphic("abba", "abab") == False
assert sol.isIsomorphic("a" * 50000, "b" * 50000) == True
assert sol.isIsomorphic("bbbaaaba", "aaabbbba") == False