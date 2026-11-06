"""
Given a list arr and an integer k, where every element is at most k
positions away from its position in the sorted list, return the
elements of arr sorted ascending.

Example 1:

Input: arr = [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], k = 2
Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Explanation: 2 is at index 3 and belongs at index 1, two positions away.
No element is further than two positions from its place.

Example 2:

Input: arr = [1, 0], k = 1
Output: [0, 1]

Example 3:

Input: arr = [1], k = 0
Output: [1]

Constraints:

    1 <= len(arr) <= 10^5
    0 <= k < len(arr)
    -10^9 <= arr[i] <= 10^9

    REQUIRED: O(n log k) time, O(k) extra space. NO sorted(), NO
    list.sort(), NO insertion sort.
"""


class Solution:
    def sort_k_messed_array(self, arr: list[int], k: int) -> list[int]:
        pass


sol = Solution()

print(sol.sort_k_messed_array([1, 4, 5, 2, 3, 7, 8, 6, 10, 9], 2))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# assert sol.sort_k_messed_array([1, 4, 5, 2, 3, 7, 8, 6, 10, 9], 2) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# assert sol.sort_k_messed_array([1, 0], 1) == [0, 1]
# assert sol.sort_k_messed_array([1], 0) == [1]
# assert sol.sort_k_messed_array([1, 0, 3, 2], 1) == [0, 1, 2, 3]
# assert sol.sort_k_messed_array([1, 0, 3, 2, 4, 5, 7, 6, 8], 1) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
# assert sol.sort_k_messed_array([6, 1, 4, 11, 2, 0, 3, 7, 10, 5, 8, 9], 6) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# assert sol.sort_k_messed_array([3, 2, 1], 2) == [1, 2, 3]
# assert sol.sort_k_messed_array([1, 2, 3], 0) == [1, 2, 3]
# assert sol.sort_k_messed_array([2, 2, 1, 1], 2) == [1, 1, 2, 2]
# assert sol.sort_k_messed_array([-1, -3, -2], 1) == [-3, -2, -1]
# assert sol.sort_k_messed_array([v for k in range(0, 10 ** 5, 2) for v in (k + 1, k)], 1) == list(range(10 ** 5))
# assert sol.sort_k_messed_array(list(range(10 ** 5)), 10 ** 5 - 1) == list(range(10 ** 5))
