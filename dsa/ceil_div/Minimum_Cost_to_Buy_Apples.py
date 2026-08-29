"""
# Minimum Cost to Buy Apples

#### Description
You need to buy at least `n` apples to make a recipe. Apples are sold in packs containing exactly `k` apples each, and each pack costs `p` dollars. You cannot buy partial packs. Return the *minimum cost* to buy at least `n` apples.

Note: It is acceptable to buy more than `n` apples if necessary, as long as you have at least `n`.

#### Example 1:
**Input:** n = 10, k = 3, p = 5
**Output:** 20
**Explanation:**
You need at least 10 apples. Buying 3 packs gives 9 apples (cost 15), which is not enough. Buying 4 packs gives 12 apples (cost 20), which is sufficient.

#### Example 2:
**Input:** n = 6, k = 3, p = 5
**Output:** 10
**Explanation:**
Buying 2 packs gives exactly 6 apples (cost 10).

#### Example 3:
**Input:** n = 1, k = 1, p = 1
**Output:** 1

#### Constraints:
- `1 <= n <= 10^9`
- `1 <= k <= 10^9`
- `1 <= p <= 10^9`
"""


class Solution:
    def minCost(self, n: int, k: int, p: int) -> int:
        ceil_div = lambda a, b: (a + b - 1) // b
        return ceil_div(n, k) * p


# Test cases
assert Solution().minCost(10, 3, 5) == 20
assert Solution().minCost(6, 3, 5) == 10
assert Solution().minCost(1, 1, 1) == 1
assert Solution().minCost(5, 3, 2) == 4
assert Solution().minCost(1000000000, 1, 1) == 1000000000
assert Solution().minCost(1, 1000000000, 1000000000) == 1000000000
