"""
EPI 16.4 Compute the binomial coefficients

Given n and k, return C(n, k), the number of subsets of size k of a set
of size n.

Example 1:

Input: n = 5, k = 2
Output: 10

Example 2:

Input: n = 4, k = 0
Output: 1
Explanation: the empty subset is the only subset of size 0.

Example 3:

Input: n = 100, k = 50
Output: 100891344545564193334812497256

Constraints:

    0 <= k <= n <= 100

    REQUIRED: O(n * k) time and O(k) extra space. NO math.comb. NO
    factorial. NO multiplication. NO division.
"""


class Solution:
    def compute_binomial_coefficient(self, n: int, k: int) -> int:
        pass


sol = Solution()

print(sol.compute_binomial_coefficient(5, 2))  # 10

# assert sol.compute_binomial_coefficient(5, 2) == 10
# assert sol.compute_binomial_coefficient(4, 0) == 1
# assert sol.compute_binomial_coefficient(100, 50) == 100891344545564193334812497256
# assert sol.compute_binomial_coefficient(4, 4) == 1
# assert sol.compute_binomial_coefficient(0, 0) == 1
# assert sol.compute_binomial_coefficient(1, 1) == 1
# assert sol.compute_binomial_coefficient(10, 5) == 252
# assert sol.compute_binomial_coefficient(20, 10) == 184756
# assert sol.compute_binomial_coefficient(30, 15) == 155117520
# assert sol.compute_binomial_coefficient(52, 5) == 2598960
# assert sol.compute_binomial_coefficient(100, 1) == 100
# assert sol.compute_binomial_coefficient(100, 99) == 100
# assert sol.compute_binomial_coefficient(100, 100) == 1
