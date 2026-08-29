"""
# Minimum Days to Eat All Oranges

#### Description

There are `n` oranges in the kitchen and you want to eat all of them. In one day, you can eat up to `k` oranges. Return the *minimum number of days* you need to eat all the oranges.

Note: You cannot eat a fraction of an orange, and you must eat all `n` oranges.

#### Example 1:
**Input:** n = 10, k = 3
**Output:** 4
**Explanation:**
- Day 1: Eat 3 oranges (remaining: 7)
- Day 2: Eat 3 oranges (remaining: 4)
- Day 3: Eat 3 oranges (remaining: 1)
- Day 4: Eat 1 orange (remaining: 0)
Total days: 4

#### Example 2:
**Input:** n = 6, k = 3
**Output:** 2
**Explanation:**
- Day 1: Eat 3 oranges
- Day 2: Eat 3 oranges

#### Example 3:
**Input:** n = 1, k = 1
**Output:** 1

#### Constraints:
- `1 <= n <= 10^9`
- `1 <= k <= 10^9`
"""


class Solution:
    def minDays(self, n: int, k: int) -> int:
        ceil_div = lambda a, b: (a + b - 1) // b
        return ceil_div(n, k)


assert Solution().minDays(10, 3) == 4
assert Solution().minDays(6, 3) == 2
assert Solution().minDays(1, 1) == 1
assert Solution().minDays(0, 5) == 0
assert Solution().minDays(1000000000, 1) == 1000000000
assert Solution().minDays(5, 10) == 1
