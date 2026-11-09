"""
EPI 14.6 Find the closest entries in three sorted arrays

Given a list sorted_arrays of sorted arrays, return the smallest
possible difference between the largest and the smallest entry of a
pick. A pick takes one entry from each array.

Example 1:

Input: sorted_arrays = [[1, 4, 10], [2, 15, 20], [10, 12]]
Output: 5
Explanation: the picks 10, 15 and 10 give 15 - 10 = 5. The picks 4, 2
and 10 give 8.

Example 2:

Input: sorted_arrays = [[3], [3], [3]]
Output: 0

Example 3:

Input: sorted_arrays = [[1, 2, 3], [100]]
Output: 97

Constraints:

    1 <= len(sorted_arrays) <= 10^3
    1 <= len(sorted_arrays[i]) <= 10^5
    The total number of entries n is at most 10^5.
    -10^9 <= sorted_arrays[i][j] <= 10^9
    Each array is in non-decreasing order.

    REQUIRED: O(n log k) time for n entries in k arrays, O(k) extra
    space. NO itertools.product. NO merged copy of the arrays.
"""


class Solution:
    def find_closest_elements_in_sorted_arrays(self, sorted_arrays: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.find_closest_elements_in_sorted_arrays([[1, 4, 10], [2, 15, 20], [10, 12]]))  # 5

# assert sol.find_closest_elements_in_sorted_arrays([[1, 4, 10], [2, 15, 20], [10, 12]]) == 5
# assert sol.find_closest_elements_in_sorted_arrays([[3], [3], [3]]) == 0
# assert sol.find_closest_elements_in_sorted_arrays([[1, 2, 3], [100]]) == 97
# assert sol.find_closest_elements_in_sorted_arrays([[7]]) == 0
# assert sol.find_closest_elements_in_sorted_arrays([[1, 5, 9]]) == 0
# assert sol.find_closest_elements_in_sorted_arrays([[1], [2], [3]]) == 2
# assert sol.find_closest_elements_in_sorted_arrays([[1, 100], [99, 200], [101, 300]]) == 2
# assert sol.find_closest_elements_in_sorted_arrays([[1, 100], [2, 200], [3, 300]]) == 2
# assert sol.find_closest_elements_in_sorted_arrays([[-10, -5, 0], [-6, 8], [-4, 20]]) == 2
# assert sol.find_closest_elements_in_sorted_arrays([[5, 5, 5], [1, 5], [5, 9]]) == 0
# assert sol.find_closest_elements_in_sorted_arrays([[-10 ** 9], [10 ** 9]]) == 2 * 10 ** 9
# assert sol.find_closest_elements_in_sorted_arrays([list(range(0, 30000, 3)), list(range(1, 30000, 3)), list(range(2, 30000, 3))]) == 2
# assert sol.find_closest_elements_in_sorted_arrays([list(range(0, 10 ** 5 - 10, 10)), list(range(5, 10 ** 5 - 10, 10)), [10 ** 5 + 7]]) == 27
# assert sol.find_closest_elements_in_sorted_arrays([[i, i + 1000] for i in range(100)]) == 99
# assert sol.find_closest_elements_in_sorted_arrays([[i] for i in range(1000)]) == 999
