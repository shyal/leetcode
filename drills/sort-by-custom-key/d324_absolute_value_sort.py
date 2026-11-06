"""
Given a list of integers arr, return its elements sorted by absolute
value, smallest first. When two elements have the same absolute value,
the negative one comes first.

Example 1:

Input: arr = [2, -7, -2, -2, 0]
Output: [0, -2, -2, 2, -7]
Explanation: -2 and 2 share the absolute value 2, so both -2 come before
the 2.

Example 2:

Input: arr = [-2, 1]
Output: [1, -2]

Example 3:

Input: arr = []
Output: []

Constraints:

    0 <= len(arr) <= 10^5
    -10^9 <= arr[i] <= 10^9

    REQUIRED: O(n log n) time, one sort. NO cmp_to_key.
"""


class Solution:
    def absSort(self, arr: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.absSort([2, -7, -2, -2, 0]))  # [0, -2, -2, 2, -7]

# assert sol.absSort([2, -7, -2, -2, 0]) == [0, -2, -2, 2, -7]
# assert sol.absSort([-2, 1]) == [1, -2]
# assert sol.absSort([]) == []
# assert sol.absSort([0, 1, 2]) == [0, 1, 2]
# assert sol.absSort([2, -1, -1, -1]) == [-1, -1, -1, 2]
# assert sol.absSort([-2, 3, 5, -1, 4]) == [-1, -2, 3, 4, 5]
# assert sol.absSort([4, -1, 6, -4, 2, -1]) == [-1, -1, 2, -4, 4, 6]
# assert sol.absSort([6, 4, -5, 0, -1, 7, 0]) == [0, 0, -1, 4, -5, 6, 7]
# assert sol.absSort([-7, -2, -2, 6, 5, -6, -2, -6]) == [-2, -2, -2, 5, -6, -6, 6, -7]
# assert sol.absSort([-4, 9, -1, 1, -1, 2, -8, -6, 3]) == [-1, -1, 1, 2, 3, -4, -6, -8, 9]
# assert sol.absSort([5]) == [5]
# assert sol.absSort([-5]) == [-5]
# assert sol.absSort([3, -3]) == [-3, 3]
# assert sol.absSort([-3, 3]) == [-3, 3]
# assert sol.absSort([10 ** 9, -10 ** 9, 0]) == [0, -10 ** 9, 10 ** 9]
# assert sol.absSort(list(range(-50000, 50000))) == [0] + [v for k in range(1, 50000) for v in (-k, k)] + [-50000]
