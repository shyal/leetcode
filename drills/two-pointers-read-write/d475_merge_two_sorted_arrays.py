"""
EPI 13.2 Merge two sorted arrays

Given a list of integers A of length m + n whose first m entries are
sorted in nondecreasing order, and a sorted list B of n integers, merge
B into A in place. After the call, A holds all m + n values in
nondecreasing order. The last n entries of A are free space before the
call, and their values do not matter.

Example 1:

Input: A = [3, 5, 9, 0, 0, 0], m = 3, B = [1, 5, 10], n = 3
Output: A becomes [1, 3, 5, 5, 9, 10]

Example 2:

Input: A = [0, 0], m = 0, B = [4, 6], n = 2
Output: A becomes [4, 6]

Example 3:

Input: A = [2, 8], m = 2, B = [], n = 0
Output: A stays [2, 8]

Constraints:

    0 <= m, n <= 10^5
    len(A) == m + n and len(B) == n
    -10^9 <= A[i], B[j] <= 10^9

    REQUIRED: O(m + n) time and O(1) extra space. NO sorting. NO new
    list.
"""


class Solution:
    def merge_two_sorted_arrays(self, A: list[int], m: int, B: list[int], n: int) -> None:
        pass


sol = Solution()

A = [3, 5, 9, 0, 0, 0]
sol.merge_two_sorted_arrays(A, 3, [1, 5, 10], 3)
print(A)  # [1, 3, 5, 5, 9, 10]

# A = [3, 5, 9, 0, 0, 0]
# sol.merge_two_sorted_arrays(A, 3, [1, 5, 10], 3)
# assert A == [1, 3, 5, 5, 9, 10]
# A = [0, 0]
# sol.merge_two_sorted_arrays(A, 0, [4, 6], 2)
# assert A == [4, 6]
# A = [2, 8]
# sol.merge_two_sorted_arrays(A, 2, [], 0)
# assert A == [2, 8]
# A = []
# sol.merge_two_sorted_arrays(A, 0, [], 0)
# assert A == []
# A = [5, 0]
# sol.merge_two_sorted_arrays(A, 1, [1], 1)
# assert A == [1, 5]
# A = [1, 0]
# sol.merge_two_sorted_arrays(A, 1, [5], 1)
# assert A == [1, 5]
# A = [4, 5, 6, 0, 0, 0]
# sol.merge_two_sorted_arrays(A, 3, [1, 2, 3], 3)
# assert A == [1, 2, 3, 4, 5, 6]
# A = [1, 2, 3, 0, 0]
# sol.merge_two_sorted_arrays(A, 3, [7, 8], 2)
# assert A == [1, 2, 3, 7, 8]
# A = [2, 2, 2, 0, 0]
# sol.merge_two_sorted_arrays(A, 3, [2, 2], 2)
# assert A == [2, 2, 2, 2, 2]
# A = [-5, 0, 7, 0, 0, 0]
# sol.merge_two_sorted_arrays(A, 3, [-6, 0, 8], 3)
# assert A == [-6, -5, 0, 0, 7, 8]
# A = list(range(0, 2 * 10 ** 5, 2)) + [0] * 10 ** 5
# sol.merge_two_sorted_arrays(A, 10 ** 5, list(range(1, 2 * 10 ** 5, 2)), 10 ** 5)
# assert A == list(range(2 * 10 ** 5))
# A = list(range(10 ** 5, 2 * 10 ** 5)) + [0] * 10 ** 5
# sol.merge_two_sorted_arrays(A, 10 ** 5, list(range(10 ** 5)), 10 ** 5)
# assert A == list(range(2 * 10 ** 5))
