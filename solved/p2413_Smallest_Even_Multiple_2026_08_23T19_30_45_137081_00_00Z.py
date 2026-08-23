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
        i = 0
        while True:
            i += 1
            if i % 2 == 0 and i % n == 0:
                return i


sol = Solution()

# print(sol.smallestEvenMultiple(5))  # 10

assert sol.smallestEvenMultiple(5) == 10
assert sol.smallestEvenMultiple(6) == 6

assert Solution().smallestEvenMultiple(1) == 2
assert Solution().smallestEvenMultiple(2) == 2
assert Solution().smallestEvenMultiple(3) == 6
assert Solution().smallestEvenMultiple(149) == 298
assert Solution().smallestEvenMultiple(150) == 150
assert Solution().smallestEvenMultiple(100) == 100
assert Solution().smallestEvenMultiple(99) == 198
assert Solution().smallestEvenMultiple(50) == 50
assert Solution().smallestEvenMultiple(51) == 102
assert Solution().smallestEvenMultiple(75) == 150
assert Solution().smallestEvenMultiple(1) == 2
assert Solution().smallestEvenMultiple(150) == 150
