"""
Given a list weights, a list values and an integer capacity, return the
largest total value of a set of items whose total weight is at most
capacity. Item i weighs weights[i] and is worth values[i]. Each item goes
in the set at most once.

Example 1:

Input: weights = [10, 20, 30], values = [60, 100, 120], capacity = 50
Output: 220
Explanation: items 1 and 2, weight 50, value 220. Taking the items with
the most value per unit of weight first gives items 0 and 1, value 160.

Example 2:

Input: weights = [4, 5, 1], values = [1, 2, 3], capacity = 4
Output: 3
Explanation: item 2 alone. Item 1 does not fit, and item 0 fills the bag
for a value of 1.

Example 3:

Input: weights = [3], values = [7], capacity = 2
Output: 0
Explanation: the one item does not fit.

Constraints:

    1 <= len(weights) == len(values) <= 100
    1 <= weights[i], values[i] <= 1000
    0 <= capacity <= 1000

    REQUIRED: O(len(weights) * capacity) time. NO most-value-per-weight
    first. NO enumeration of every subset of the items.

This is the 0/1 knapsack.
"""


class Solution:
    def knapsack(self, weights: list[int], values: list[int], capacity: int) -> int:
        pass


sol = Solution()

print(sol.knapsack([10, 20, 30], [60, 100, 120], 50))  # 220

# assert sol.knapsack([10, 20, 30], [60, 100, 120], 50) == 220
# assert sol.knapsack([4, 5, 1], [1, 2, 3], 4) == 3
# assert sol.knapsack([3], [7], 2) == 0
# assert sol.knapsack([1, 1, 1], [10, 20, 30], 2) == 50
# assert sol.knapsack([4, 2, 3], [10, 20, 15], 5) == 35
# assert sol.knapsack([2], [5], 2) == 5
# assert sol.knapsack([1, 2, 3], [1, 2, 3], 0) == 0
# assert sol.knapsack([1, 2, 3], [4, 5, 6], 6) == 15
# assert sol.knapsack([1, 2, 3], [4, 5, 6], 5) == 11
# assert sol.knapsack([5, 4, 6, 3], [10, 40, 30, 50], 10) == 90
# assert sol.knapsack([1000], [1000], 1000) == 1000
# assert sol.knapsack([1000], [1000], 999) == 0
# assert sol.knapsack([10] * 100, [10] * 100, 1000) == 1000
# assert sol.knapsack([10] * 100, [10] * 100, 995) == 990
# assert sol.knapsack(list(range(1, 101)), list(range(1, 101)), 1000) == 1000
# assert sol.knapsack(list(range(1, 101)), [1000 - i for i in range(100)], 1000) == 43054
