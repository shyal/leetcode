"""
Given a list arr of item weights and an integer limit, return [i, j],
the indices of two items whose weights sum to limit, with j < i. If no
two items sum to limit, return []. When several pairs sum to limit, i
is the smallest index that has a partner before it, and j is the
largest index among the partners of i.

Example 1:

Input: arr = [4, 6, 10, 15, 16], limit = 21
Output: [3, 1]
Explanation: 15 + 6 = 21, at indices 3 and 1.

Example 2:

Input: arr = [4, 4, 1], limit = 5
Output: [2, 1]
Explanation: item 2 pairs with item 0 and with item 1. The larger
partner index is 1.

Example 3:

Input: arr = [9], limit = 9
Output: []
Explanation: an item cannot pair with itself.

Constraints:

    0 <= len(arr) <= 100
    0 <= arr[i] <= 10^4
    0 <= limit <= 2 * 10^4

    REQUIRED: O(n) time. NO nested loops over index pairs, NO sort.
"""


class Solution:
    def get_indices_of_item_weights(self, arr: list[int], limit: int) -> list[int]:
        pass


sol = Solution()

print(sol.get_indices_of_item_weights([4, 6, 10, 15, 16], 21))  # [3, 1]

# assert sol.get_indices_of_item_weights([4, 6, 10, 15, 16], 21) == [3, 1]
# assert sol.get_indices_of_item_weights([4, 4, 1], 5) == [2, 1]
# assert sol.get_indices_of_item_weights([9], 9) == []
# assert sol.get_indices_of_item_weights([4, 4], 8) == [1, 0]
# assert sol.get_indices_of_item_weights([4, 6, 10, 15, 16], 20) == [4, 0]
# assert sol.get_indices_of_item_weights([12, 6, 7, 14, 19, 3, 0, 25, 40], 7) == [6, 2]
# assert sol.get_indices_of_item_weights([], 5) == []
# assert sol.get_indices_of_item_weights([0, 0], 0) == [1, 0]
# assert sol.get_indices_of_item_weights([5, 5, 5], 10) == [1, 0]
# assert sol.get_indices_of_item_weights([1, 2, 3, 4, 5], 9) == [4, 3]
# assert sol.get_indices_of_item_weights([1, 2, 3, 4, 5], 5) == [2, 1]
# assert sol.get_indices_of_item_weights(list(range(100)), 197) == [99, 98]
# assert sol.get_indices_of_item_weights(list(range(100)), 1) == [1, 0]
# assert sol.get_indices_of_item_weights(list(range(100)), 198) == []
# assert sol.get_indices_of_item_weights([10000] * 100, 20000) == [1, 0]
