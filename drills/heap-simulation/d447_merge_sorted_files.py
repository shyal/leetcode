"""
EPI 10.1 Merge sorted files

Given a list sorted_arrays of k lists, each sorted ascending, return one
list of all their elements, sorted ascending.

Example 1:

Input: sorted_arrays = [[2, 9, 14], [1, 10], [5, 9, 30]]
Output: [1, 2, 5, 9, 9, 10, 14, 30]

Example 2:

Input: sorted_arrays = [[], [4], []]
Output: [4]

Example 3:

Input: sorted_arrays = []
Output: []

Constraints:

    0 <= k <= 10^4
    0 <= n <= 10^5, where n is the total number of elements
    -10^9 <= sorted_arrays[i][j] <= 10^9

    REQUIRED: O(n log k) time and O(k) extra space, the output not
    counted. NO sorted(), NO list.sort(), NO heapq.merge().
"""


class Solution:
    def merge_sorted_arrays(self, sorted_arrays: list[list[int]]) -> list[int]:
        pass


sol = Solution()

print(sol.merge_sorted_arrays([[2, 9, 14], [1, 10], [5, 9, 30]]))  # [1, 2, 5, 9, 9, 10, 14, 30]

# assert sol.merge_sorted_arrays([[2, 9, 14], [1, 10], [5, 9, 30]]) == [1, 2, 5, 9, 9, 10, 14, 30]
# assert sol.merge_sorted_arrays([[], [4], []]) == [4]
# assert sol.merge_sorted_arrays([]) == []
# assert sol.merge_sorted_arrays([[]]) == []
# assert sol.merge_sorted_arrays([[1, 2, 3]]) == [1, 2, 3]
# assert sol.merge_sorted_arrays([[5], [4], [3], [2], [1]]) == [1, 2, 3, 4, 5]
# assert sol.merge_sorted_arrays([[1, 1, 1], [1, 1]]) == [1, 1, 1, 1, 1]
# assert sol.merge_sorted_arrays([[-3, 0, 7], [-5, 8], [-4, -4, 9]]) == [-5, -4, -4, -3, 0, 7, 8, 9]
# assert sol.merge_sorted_arrays([[10, 20], [1, 2, 3, 4, 5]]) == [1, 2, 3, 4, 5, 10, 20]
# assert sol.merge_sorted_arrays([[1, 4, 7], [2, 5, 8], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
# assert sol.merge_sorted_arrays([[0], [], [0], []]) == [0, 0]
# assert sol.merge_sorted_arrays([list(range(i, 10 ** 5, 100)) for i in range(100)]) == list(range(10 ** 5))
# assert sol.merge_sorted_arrays([[i] for i in range(10 ** 4 - 1, -1, -1)]) == list(range(10 ** 4))
