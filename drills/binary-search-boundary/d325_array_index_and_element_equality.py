"""
Given a sorted array arr of distinct integers, return the lowest index i
for which arr[i] == i. Return -1 when no index satisfies it.

Example 1:

Input: arr = [-5, 1, 2, 4]
Output: 1
Explanation: arr[1] == 1 and arr[2] == 2. The lowest is 1.

Example 2:

Input: arr = [-8, 0, 2, 5]
Output: 2

Example 3:

Input: arr = [-1, 0, 3, 6]
Output: -1
Explanation: no index i has arr[i] == i.

Constraints:

    1 <= len(arr) <= 10^5
    -10^9 <= arr[i] <= 10^9
    arr is sorted in increasing order and its values are distinct.

    REQUIRED: O(log n) time, O(1) extra space. NO linear scan.
"""


class Solution:
    def index_equals_value_search(self, arr: list[int]) -> int:
        pass


sol = Solution()

print(sol.index_equals_value_search([-5, 1, 2, 4]))  # 1

# assert sol.index_equals_value_search([-5, 1, 2, 4]) == 1
# assert sol.index_equals_value_search([-8, 0, 2, 5]) == 2
# assert sol.index_equals_value_search([-1, 0, 3, 6]) == -1
# assert sol.index_equals_value_search([0]) == 0
# assert sol.index_equals_value_search([0, 3]) == 0
# assert sol.index_equals_value_search([-8, 0, 1, 3, 5]) == 3
# assert sol.index_equals_value_search([-5, 0, 2, 3, 10, 29]) == 2
# assert sol.index_equals_value_search([-5, 0, 3, 4, 10, 18, 27]) == -1
# assert sol.index_equals_value_search([-6, -5, -4, -1, 1, 3, 5, 7]) == 7
# assert sol.index_equals_value_search([5]) == -1
# assert sol.index_equals_value_search([-1]) == -1
# assert sol.index_equals_value_search([-3, 1]) == 1
# assert sol.index_equals_value_search(list(range(10 ** 5))) == 0
# assert sol.index_equals_value_search(list(range(1, 10 ** 5 + 1))) == -1
# assert sol.index_equals_value_search(list(range(-10 ** 5, 0))) == -1
# assert sol.index_equals_value_search([-10 ** 9] + list(range(1, 10 ** 5))) == 1
# assert sol.index_equals_value_search(list(range(-(10 ** 5) + 1, 1)) + [10 ** 5]) == 10 ** 5
