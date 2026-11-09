"""
EPI 10.2 Sort an increasing-decreasing array

Given a list A of integers, return the elements of A sorted ascending.
A goes up and down: it splits into k runs of consecutive elements, and
each run is strictly increasing or strictly decreasing. No two adjacent
elements of A are equal.

Example 1:

Input: A = [1, 4, 9, 6, 2, 3, 8, 7]
Output: [1, 2, 3, 4, 6, 7, 8, 9]
Explanation: A goes up to 9, down to 2, up to 8 and down to 7.

Example 2:

Input: A = [5, 4, 3]
Output: [3, 4, 5]

Example 3:

Input: A = [7]
Output: [7]

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    A[i] != A[i + 1]

    REQUIRED: O(n log k) time, where k is the number of runs. NO
    sorted(), NO list.sort(), NO heapq.merge().
"""


class Solution:
    def sort_k_increasing_decreasing_array(self, A: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.sort_k_increasing_decreasing_array([1, 4, 9, 6, 2, 3, 8, 7]))  # [1, 2, 3, 4, 6, 7, 8, 9]

# assert sol.sort_k_increasing_decreasing_array([1, 4, 9, 6, 2, 3, 8, 7]) == [1, 2, 3, 4, 6, 7, 8, 9]
# assert sol.sort_k_increasing_decreasing_array([5, 4, 3]) == [3, 4, 5]
# assert sol.sort_k_increasing_decreasing_array([7]) == [7]
# assert sol.sort_k_increasing_decreasing_array([]) == []
# assert sol.sort_k_increasing_decreasing_array([1, 2, 3]) == [1, 2, 3]
# assert sol.sort_k_increasing_decreasing_array([2, 1]) == [1, 2]
# assert sol.sort_k_increasing_decreasing_array([1, 2]) == [1, 2]
# assert sol.sort_k_increasing_decreasing_array([3, 1, 2]) == [1, 2, 3]
# assert sol.sort_k_increasing_decreasing_array([1, 3, 2, 4, 0, 5]) == [0, 1, 2, 3, 4, 5]
# assert sol.sort_k_increasing_decreasing_array([9, 1, 8, 2, 7, 3]) == [1, 2, 3, 7, 8, 9]
# assert sol.sort_k_increasing_decreasing_array([-1, 5, -2, 6, -4, 0]) == [-4, -2, -1, 0, 5, 6]
# assert sol.sort_k_increasing_decreasing_array([10, 20, 30, 25, 15, 5, 12, 40]) == [5, 10, 12, 15, 20, 25, 30, 40]
# assert sol.sort_k_increasing_decreasing_array([4, 1, 4, 1, 4]) == [1, 1, 4, 4, 4]
# assert sol.sort_k_increasing_decreasing_array(list(range(50000)) + list(range(10 ** 5, 50000, -1))) == list(range(50000)) + list(range(50001, 10 ** 5 + 1))
# assert sol.sort_k_increasing_decreasing_array([v for i in range(1000) for v in (range(100 * (37 * i % 1000), 100 * (37 * i % 1000) + 100) if i % 2 == 0 else range(100 * (37 * i % 1000) + 99, 100 * (37 * i % 1000) - 1, -1))]) == list(range(10 ** 5))
