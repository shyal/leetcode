"""
Given two positions a and b on a ring of m positions numbered 0 to m -
1, where position 0 and position m - 1 are adjacent, return the smallest
number of steps from a to b. A step moves to an adjacent position in
either direction.

Take the difference abs(a - b): that is the number of steps the direct
way round. The other way round is m minus that. Return the smaller.

For example with a = 1, b = 9 and m = 10, the direct way is 8 steps and
the other way is 2 steps: 1 to 0 to 9. The answer is 2.

Example 1:

Input: a = 1, b = 9, m = 10
Output: 2

Example 2:

Input: a = 3, b = 7, m = 10
Output: 4

Example 3:

Input: a = 0, b = 5, m = 10
Output: 5
Explanation: both ways round take 5 steps.

Constraints:

    2 <= m <= 10^9
    0 <= a, b < m

    REQUIRED: O(1), arithmetic only. NO loop around the ring. The
    direct difference alone is the failure mode this drill exists to
    kill: it returns 8 on a = 1, b = 9, m = 10.
"""


class Solution:
    def dist(self, a: int, b: int, m: int) -> int:
        pass


sol = Solution()

print(sol.dist(1, 9, 10))  # 2

# assert sol.dist(1, 9, 10) == 2
# assert sol.dist(3, 7, 10) == 4
# assert sol.dist(0, 5, 10) == 5
# assert sol.dist(9, 1, 10) == 2
# assert sol.dist(4, 4, 10) == 0
# assert sol.dist(0, 9, 10) == 1
# assert sol.dist(9, 0, 10) == 1
# assert sol.dist(0, 1, 2) == 1
# assert sol.dist(0, 10 ** 9 - 1, 10 ** 9) == 1
# assert sol.dist(0, 10 ** 9 // 2, 10 ** 9) == 10 ** 9 // 2
# assert sol.dist(2, 11, 12) == 3
