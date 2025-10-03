"""
URL: https://leetcode.com/problems/smallest-even-multiple/description/?envType=problem-list-v2&envId=vn57k9wr

2413. Smallest Even Multiple

Given a positive integer n, return the smallest positive integer that is a multiple of both 2 and n.


Example 1:

Input: n = 5
Output: 10
Explanation: The smallest multiple of both 5 and 2 is 10.

Example 2:

Input: n = 6
Output: 6
Explanation: The smallest multiple of both 6 and 2 is 6. Note that a number is a multiple of itself.


Constraints:

    1 <= n <= 150
"""


class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        i = 1
        while True:
            if i % 2 == 0 and i % n == 0:
                return i
            i += 1


sol = Solution()

assert sol.smallestEvenMultiple(5) == 10
assert sol.smallestEvenMultiple(6) == 6
