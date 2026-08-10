"""
URL: https://leetcode.com/problems/smallest-even-multiple/description/?envType=problem-list-v2&envId=vn57k9wr

2413. Smallest Even Multiple

Given a positive integer n, return the smallest positive integer that is a
multiple of both 2 and n.


Example 1:

Input: n = 5
Output: 10
Explanation: The smallest multiple of both 5 and 2 is 10.

Example 2:

Input: n = 6
Output: 6
Explanation: The smallest multiple of both 6 and 2 is 6. Note that a number is
a multiple of itself.


Constraints:

    1 <= n <= 150
"""


class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        return n if n % 2 == 0 else n * 2


sol = Solution()

assert sol.smallestEvenMultiple(5) == 10
assert sol.smallestEvenMultiple(6) == 6
assert sol.smallestEvenMultiple(1) == 2
assert sol.smallestEvenMultiple(150) == 150

assert sol.smallestEvenMultiple(2) == 2
assert sol.smallestEvenMultiple(3) == 6
assert sol.smallestEvenMultiple(4) == 4
assert sol.smallestEvenMultiple(7) == 14
assert sol.smallestEvenMultiple(8) == 8
assert sol.smallestEvenMultiple(9) == 18
assert sol.smallestEvenMultiple(10) == 10
assert sol.smallestEvenMultiple(15) == 30
assert sol.smallestEvenMultiple(16) == 16
assert sol.smallestEvenMultiple(75) == 150
assert sol.smallestEvenMultiple(100) == 100
assert sol.smallestEvenMultiple(127) == 254
assert sol.smallestEvenMultiple(128) == 128
assert sol.smallestEvenMultiple(148) == 148
assert sol.smallestEvenMultiple(149) == 298

for _n in range(1, 151):
    _r = sol.smallestEvenMultiple(_n)
    _brute = next(m for m in range(1, 2 * _n + 1) if m % 2 == 0 and m % _n == 0)
    assert _r == _brute
    assert _r % 2 == 0
    assert _r % _n == 0
    assert _r > 0
    assert _r == (_n if _n % 2 == 0 else 2 * _n)
    assert _n <= _r <= 2 * _n

assert all(sol.smallestEvenMultiple(_n) == _n for _n in range(2, 151, 2))
assert all(sol.smallestEvenMultiple(_n) == 2 * _n for _n in range(1, 151, 2))