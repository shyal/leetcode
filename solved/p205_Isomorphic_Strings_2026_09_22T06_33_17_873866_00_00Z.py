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


"abcabc", "xyzyxz"

"abcabc", "abcbac"

Close. I just had:

                if b in paired_with.values():
                    return False

In the wrong block.

Assisted.

LEETCODE: Accepted (15 ms, 22.5 MB)
"""


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        z = [*zip(s, t)]
        print(z)
        paired_with = {}
        used = set([])
        for a, b in z:
            if a not in paired_with:
                if b in paired_with.values():
                    return False
                paired_with[a] = b
            else:
                if paired_with[a] != b:
                    return False

        print(paired_with)
        return True


sol = Solution()

print(sol.isIsomorphic("abcabc", "xyzyxz"))

# # sol.isIsomorphic("paper", "title") is True

print(sol.isIsomorphic("egg", "add"))  # True

assert sol.isIsomorphic("egg", "add") is True
assert sol.isIsomorphic("foo", "bar") is False
assert sol.isIsomorphic("paper", "title") is True

assert sol.isIsomorphic("", "") == True
assert sol.isIsomorphic("a", "a") == True
assert sol.isIsomorphic("a", "b") == True
assert sol.isIsomorphic("abc", "def") == True
assert sol.isIsomorphic("abc", "dee") == False
assert sol.isIsomorphic("aaa", "bbb") == True
assert sol.isIsomorphic("abcabc", "xyzxyz") == True
assert sol.isIsomorphic("abcabc", "xyzyxz") == False
assert (
    sol.isIsomorphic("abcdefghijklmnopqrstuvwxyz", "bcdefghijklmnopqrstuvwxyza") == True
)
# assert (
#     sol.isIsomorphic(
#         "abcdefghijklmnopqrstuvwxyz" * 2000, "bcdefghijklmnopqrstuvwxyza" * 2000
#     )
#     == True
# )
assert sol.isIsomorphic("12345", "54321") == True
assert sol.isIsomorphic("!@#$%", "%$#@!") == True
