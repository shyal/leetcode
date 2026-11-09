"""
EPI 12.11 Test the Collatz conjecture

Given a positive integer n, return True when every integer from 1 to n
reaches 1 under the Collatz rule, and False when some integer in that
range does not. The Collatz rule maps x to x / 2 when x is even and to
3x + 1 when x is odd. The integer 1 reaches 1 with zero steps.

Example 1:

Input: n = 6
Output: True
Explanation: 6 gives 3, 10, 5, 16, 8, 4, 2, 1. Each of 1 to 5 also
reaches 1.

Example 2:

Input: n = 1
Output: True

Example 3:

Input: n = 27
Output: True
Explanation: 27 takes 111 steps and goes up to 9232 before it reaches 1.

Constraints:

    1 <= n <= 10^6

    REQUIRED: n = 10^6 must finish in under 2 seconds.
"""


class Solution:
    def test_collatz_conjecture(self, n: int) -> bool:
        pass


sol = Solution()

print(sol.test_collatz_conjecture(6))  # True

# assert sol.test_collatz_conjecture(6) is True
# assert sol.test_collatz_conjecture(1) is True
# assert sol.test_collatz_conjecture(27) is True
# assert sol.test_collatz_conjecture(2) is True
# assert sol.test_collatz_conjecture(3) is True
# assert sol.test_collatz_conjecture(7) is True
# assert sol.test_collatz_conjecture(100) is True
# assert sol.test_collatz_conjecture(1000) is True
# assert sol.test_collatz_conjecture(10 ** 5) is True
# assert sol.test_collatz_conjecture(10 ** 6) is True
