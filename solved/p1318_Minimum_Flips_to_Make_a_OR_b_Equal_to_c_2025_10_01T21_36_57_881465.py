"""
URL: https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/description/?envType=study-plan-v2&envId=leetcode-75

1318. Minimum Flips to Make a OR b Equal to c

Given 3 positives numbers a, b and c. Return the minimum flips required in some bits of a and b to make ( a OR b == c ). (bitwise OR operation).
Flip operation consists of change any single bit 1 to 0 or change the bit 0 to 1 in their binary representation.


Example 1:

Input: a = 2, b = 6, c = 5
Output: 3
Explanation: After flips a = 1 , b = 4 , c = 5 such that (a OR b == c)

Example 2:

Input: a = 4, b = 2, c = 7
Output: 1

Example 3:

Input: a = 1, b = 2, c = 3
Output: 0


Constraints:

        1 <= a <= 10^9
        1 <= b <= 10^9
        1 <= c <= 10^9
"""


class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        count = 0
        while a or b or c:
            _a, _b, _c = a & 1, b & 1, c & 1
            _ab = _a + _b
            count += (not _ab) if _c else _ab
            a, b, c = a >> 1, b >> 1, c >> 1
        return count


sol = Solution()
assert sol.minFlips(a=2, b=6, c=5) == 3
assert sol.minFlips(a=4, b=2, c=7) == 1
assert sol.minFlips(a=1, b=2, c=3) == 0
assert sol.minFlips(a=1, b=1, c=1) == 0
assert sol.minFlips(a=8, b=1, c=1) == 1
assert sol.minFlips(a=3, b=3, c=1) == 2
assert sol.minFlips(a=1, b=1, c=3) == 1
assert sol.minFlips(a=1, b=2, c=4) == 3
assert sol.minFlips(a=7, b=7, c=1) == 4
