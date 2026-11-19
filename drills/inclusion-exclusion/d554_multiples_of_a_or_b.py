"""
Given three positive integers n, a and b, return the number of integers x
with 1 <= x <= n such that a divides x or b divides x.

Example 1:

Input: n = 10, a = 2, b = 3
Output: 7
Explanation: The integers are 2, 3, 4, 6, 8, 9 and 10.

Example 2:

Input: n = 12, a = 4, b = 6
Output: 4
Explanation: The integers are 4, 6, 8 and 12.

Example 3:

Input: n = 5, a = 7, b = 9
Output: 0

Use the inclusion-exclusion principle.

Constraints:

    1 <= n, a, b <= 10^12

    REQUIRED: O(log(a + b)) time. NO loop over the integers from 1 to n.
"""


class Solution:

    def multiples(self, n: int, a: int, b: int) -> int:
        pass


sol = Solution()

print(sol.multiples(10, 2, 3))  # 7

# assert sol.multiples(10, 2, 3) == 7
# assert sol.multiples(12, 4, 6) == 4
# assert sol.multiples(5, 7, 9) == 0
# assert sol.multiples(9, 3, 3) == 3
# assert sol.multiples(8, 1, 5) == 8
# assert sol.multiples(6, 2, 3) == 4
# assert sol.multiples(5, 2, 3) == 3
# assert sol.multiples(20, 2, 4) == 10
# assert sol.multiples(100, 6, 10) == 23
# assert sol.multiples(1, 1, 1) == 1
# assert sol.multiples(10**12, 2, 3) == 666666666667
# assert sol.multiples(10**12, 10**12, 10**12) == 1
