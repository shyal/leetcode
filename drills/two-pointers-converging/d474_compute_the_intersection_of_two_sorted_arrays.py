"""
EPI 13.1 Compute the intersection of two sorted arrays

Given two lists of integers A and B, each sorted in nondecreasing order,
return the sorted list of the distinct values that appear in both A and
B.

Example 1:

Input: A = [1, 2, 2, 3, 5, 8], B = [2, 2, 3, 4, 8, 8, 9]
Output: [2, 3, 8]
Explanation: 2 appears twice in both lists and is in the output once.

Example 2:

Input: A = [1, 3], B = [2, 4]
Output: []

Example 3:

Input: A = [], B = [1]
Output: []

Constraints:

    0 <= len(A), len(B) <= 10^5
    -10^9 <= A[i], B[j] <= 10^9
    A and B are sorted in nondecreasing order.

    REQUIRED: O(m + n) time, where m and n are the lengths of A and B.
    NO set or dict.
"""


class Solution:
    def intersect_two_sorted_arrays(self, A: list[int], B: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.intersect_two_sorted_arrays([1, 2, 2, 3, 5, 8], [2, 2, 3, 4, 8, 8, 9]))  # [2, 3, 8]

# assert sol.intersect_two_sorted_arrays([1, 2, 2, 3, 5, 8], [2, 2, 3, 4, 8, 8, 9]) == [2, 3, 8]
# assert sol.intersect_two_sorted_arrays([1, 3], [2, 4]) == []
# assert sol.intersect_two_sorted_arrays([], [1]) == []
# assert sol.intersect_two_sorted_arrays([], []) == []
# assert sol.intersect_two_sorted_arrays([1], [1]) == [1]
# assert sol.intersect_two_sorted_arrays([1, 1, 1], [1]) == [1]
# assert sol.intersect_two_sorted_arrays([1, 2, 3], [4, 5]) == []
# assert sol.intersect_two_sorted_arrays([1, 2, 3], [3, 4]) == [3]
# assert sol.intersect_two_sorted_arrays([5, 6], [1, 5]) == [5]
# assert sol.intersect_two_sorted_arrays([-3, -1, 0, 2], [-3, 0, 0, 7]) == [-3, 0]
# assert sol.intersect_two_sorted_arrays([1, 2, 3, 4], [1, 2, 3, 4]) == [1, 2, 3, 4]
# assert sol.intersect_two_sorted_arrays([2, 2, 2, 9], [1, 2, 9, 9]) == [2, 9]
# assert sol.intersect_two_sorted_arrays(list(range(0, 2 * 10 ** 5, 2)), list(range(0, 2 * 10 ** 5, 3))) == list(range(0, 2 * 10 ** 5, 6))
# assert sol.intersect_two_sorted_arrays([7] * 10 ** 5, [7] * 10 ** 5) == [7]
# assert sol.intersect_two_sorted_arrays(list(range(10 ** 5)), [10 ** 5 - 1]) == [10 ** 5 - 1]
