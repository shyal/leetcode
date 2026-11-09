"""
EPI 14.7 Enumerate extended integers

Given an integer k, return the k smallest numbers of the form
a + b * sqrt(2), where a and b are non-negative integers, in ascending
order, as floats.

Example 1:

Input: k = 8
Output: [0.0, 1.0, 1.414, 2.0, 2.414, 2.828, 3.0, 3.414]
Explanation: the pairs (a, b) are (0, 0), (1, 0), (0, 1), (2, 0),
(1, 1), (0, 2), (3, 0), (2, 1). The output shows three decimals.

Example 2:

Input: k = 1
Output: [0.0]

Example 3:

Input: k = 0
Output: []

Constraints:

    0 <= k <= 10^5
    Two different pairs (a, b) always give different numbers.

    REQUIRED: O(k) time. NO heap. NO sorting.
"""


class Solution:
    def generate_first_k_a_b_sqrt2(self, k: int) -> list[float]:
        pass


sol = Solution()

print([round(x, 3) for x in sol.generate_first_k_a_b_sqrt2(8)])  # [0.0, 1.0, 1.414, 2.0, 2.414, 2.828, 3.0, 3.414]

# r = sol.generate_first_k_a_b_sqrt2(8)
# assert len(r) == 8
# assert all(isclose(x, y) for x, y in zip(r, [0, 1, sqrt(2), 2, 1 + sqrt(2), 2 * sqrt(2), 3, 2 + sqrt(2)]))
# assert sol.generate_first_k_a_b_sqrt2(1) == [0.0]
# assert sol.generate_first_k_a_b_sqrt2(0) == []
# r = sol.generate_first_k_a_b_sqrt2(2)
# assert len(r) == 2 and isclose(r[1], 1)
# r = sol.generate_first_k_a_b_sqrt2(3)
# assert len(r) == 3 and isclose(r[2], sqrt(2))
# r = sol.generate_first_k_a_b_sqrt2(12)
# assert len(r) == 12
# assert all(isclose(x, y) for x, y in zip(r[8:], [1 + 2 * sqrt(2), 4, 3 * sqrt(2), 3 + sqrt(2)]))
# brute = sorted(a + b * sqrt(2) for a in range(200) for b in range(150))
# r = sol.generate_first_k_a_b_sqrt2(10 ** 4)
# assert len(r) == 10 ** 4
# assert all(isclose(x, y) for x, y in zip(r, brute))
# assert all(x < y for x, y in zip(r, r[1:]))
# r = sol.generate_first_k_a_b_sqrt2(10 ** 5)
# assert len(r) == 10 ** 5 and len(set(r)) == 10 ** 5
