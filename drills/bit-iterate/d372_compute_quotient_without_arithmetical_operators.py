"""
EPI 4.6 Compute quotient without arithmetical operators

Given a nonnegative integer x and a positive integer y, return the
quotient of x divided by y, rounded down. The only operators you may use
are addition, subtraction, the shifts << and >>, and comparisons.

Example 1:

Input: x = 23, y = 5
Output: 4
Explanation: 4 * 5 = 20 <= 23 < 25 = 5 * 5.

Example 2:

Input: x = 4, y = 9
Output: 0

Example 3:

Input: x = 2^62, y = 1
Output: 4611686018427387904

Constraints:

    0 <= x < 2^63
    1 <= y < 2^63

    REQUIRED: O(n) time, where n is the number of bits in x. NO *, NO
    /, NO //, NO %, NO **, NO divmod().
"""


class Solution:
    def divide(self, x: int, y: int) -> int:
        pass


sol = Solution()

print(sol.divide(23, 5))  # 4

# assert sol.divide(23, 5) == 4
# assert sol.divide(4, 9) == 0
# assert sol.divide(2 ** 62, 1) == 2 ** 62
# assert sol.divide(0, 1) == 0
# assert sol.divide(0, 7) == 0
# assert sol.divide(1, 1) == 1
# assert sol.divide(7, 7) == 1
# assert sol.divide(6, 7) == 0
# assert sol.divide(64, 2) == 32
# assert sol.divide(2 ** 63 - 1, 2 ** 63 - 1) == 1
# assert sol.divide(2 ** 63 - 1, 2) == 4611686018427387903
# assert sol.divide(2 ** 63 - 1, 3) == 3074457345618258602
# assert sol.divide(1000000007, 13) == 76923077
# assert all(sol.divide(a, b) == a // b for a in range(60) for b in range(1, 20))
