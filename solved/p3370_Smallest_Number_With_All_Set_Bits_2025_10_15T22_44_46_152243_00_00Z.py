"""
URL: https://leetcode.com/problems/smallest-number-with-all-set-bits/description/?envType=problem-list-v2&envId=v0n2n1sc

3370. Smallest Number With All Set Bits

You are given a positive number n.

Return the smallest number x greater than or equal to n, such that the binary representation of x contains only set bits


Example 1:

Input: n = 5

Output: 7

Explanation:

The binary representation of 7 is "111".

Example 2:

Input: n = 10

Output: 15

Explanation:

The binary representation of 15 is "1111".

Example 3:

Input: n = 3

Output: 3

Explanation:

The binary representation of 3 is "11".


Constraints:

        1 <= n <= 1000
"""


class Solution:
    def smallestNumber(self, n: int) -> int:
        r = 1
        while True:
            if r >= n:
                return r
            r = r << 1 | 1


sol = Solution()
assert sol.smallestNumber(n=5) == 7
assert sol.smallestNumber(n=10) == 15
assert sol.smallestNumber(n=3) == 3
