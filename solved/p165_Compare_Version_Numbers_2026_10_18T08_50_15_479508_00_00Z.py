"""
URL: https://leetcode.com/problems/compare-version-numbers/description/?envType=problem-list-v2&envId=vn57k9wr

165. Compare Version Numbers

Given two version strings, version1 and version2, compare them. A version string consists of revisions separated by dots '.'. The value of the revision is its integer conversion ignoring leading zeros.

To compare version strings, compare their revision values in left-to-right order. If one of the version strings has fewer revisions, treat the missing revision values as 0.

Return the following:

- If version1 < version2, return -1.
- If version1 > version2, return 1.
- Otherwise, return 0.

Example 1:

Input: version1 = "1.2", version2 = "1.10"
Output: -1
Explanation:
version1's second revision is "2" and version2's second revision is "10": 2 < 10, so version1 < version2.

Example 2:

Input: version1 = "1.01", version2 = "1.001"
Output: 0
Explanation:
Ignoring leading zeroes, both "01" and "001" represent the same integer "1".

Example 3:

Input: version1 = "1.0", version2 = "1.0.0.0"
Output: 0
Explanation:
version1 has less revisions, which means every missing revision are treated as "0".

Constraints:

    1 <= version1.length, version2.length <= 500
    version1 and version2 only contain digits and '.'.
    version1 and version2 are valid version numbers.
    All the given revisions in version1 and version2 can be stored in a 32-bit integer.

---

LEETCODE: Accepted (0 ms, 19.2 MB)
"""


# mu 0.12
# class Solution
#   def compareVersion(version1: str, version2: str) -> int
#     def ignoreTrailingZeros(s)
#       for >i, c in s
#         if c != 0
#           return s[i:]
#       s
#     def toVersion(s)
#       version = s.split('.')
#       res = []
#       for >i, v in version
#         res <- int(ignoreTrailingZeros(v))
#       res
#
#     a = toVersion(version1)
#     b = toVersion(version2)
#     a = ignoreTrailingZeros(a[::-1])[::-1]
#     b = ignoreTrailingZeros(b[::-1])[::-1]
#     # print(a)
#     # print(b)
#     if a == b
#       return 0
#     return -1 if a < b else 1

class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        def ignoreTrailingZeros(s):
            for i, c in enumerate(s):
                if c != 0:
                    return s[i:]
            return s
        def toVersion(s):
            version = s.split('.')
            res = []
            for i, v in enumerate(version):
                res.append(int(ignoreTrailingZeros(v)))
            return res
        a = toVersion(version1)
        b = toVersion(version2)
        a = ignoreTrailingZeros(a[::-1])[::-1]
        b = ignoreTrailingZeros(b[::-1])[::-1]
        if a == b:
            return 0
        return -1 if a < b else 1


sol = Solution()
print(sol.compareVersion('1.2', '1.10'))
_l, _r = sol.compareVersion('1.2', '1.10'), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.01', '1.001'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0', '1.0.0.0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('0', '0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0.0.0.0.0.0.0.0.0', '1'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0.0.0.0.0.0.0.0.0', '1.0.0.0.0.0.0.0.0.1'), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0.0.0.0.0.0.0.0.0', '1.0.0.0.0.0.0.0.0.0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0.0.0.0.0.0.0.0.0', '1.0.0.0.0.0.0.0.0.0.0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('1.0.0.0.0.0.0.0.0.0.0', '1.0.0.0.0.0.0.0.0.0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('2147483647', '2147483646'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.compareVersion('2147483647.2147483647', '2147483647.2147483646'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
