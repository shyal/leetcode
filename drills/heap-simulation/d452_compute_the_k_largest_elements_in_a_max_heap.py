"""
EPI 10.6 Compute the k largest elements in a max-heap

Given a list A that is a max-heap and an integer k, return the k largest
elements of A, in any order. A is a max-heap: for each index i,
A[i] >= A[2i + 1] and A[i] >= A[2i + 2] when those indices exist. A
must not change.

Example 1:

Input: A = [20, 14, 18, 7, 9, 3, 11, 2, 5], k = 4
Output: [20, 18, 14, 11]
Explanation: A is the tree below. 11 is at depth 2, below 18.

            20
          /    \\
        14      18
       /  \\    /  \\
      7    9  3    11
     / \\
    2   5

Example 2:

Input: A = [5], k = 1
Output: [5]

Example 3:

Input: A = [9, 9, 4], k = 2
Output: [9, 9]

Constraints:

    1 <= k <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(k log k) time and O(k) extra space. NO sorted(), NO
    list.sort(), NO heapq.nlargest(), NO change to A.
"""


class Solution:
    def k_largest_in_binary_heap(self, A: list[int], k: int) -> list[int]:
        pass


sol = Solution()

print(sol.k_largest_in_binary_heap([20, 14, 18, 7, 9, 3, 11, 2, 5], 4))  # [20, 18, 14, 11]

# assert sorted(sol.k_largest_in_binary_heap([20, 14, 18, 7, 9, 3, 11, 2, 5], 4)) == [11, 14, 18, 20]
# assert sorted(sol.k_largest_in_binary_heap([5], 1)) == [5]
# assert sorted(sol.k_largest_in_binary_heap([9, 9, 4], 2)) == [9, 9]
# assert sorted(sol.k_largest_in_binary_heap([20, 14, 18, 7, 9, 3, 11, 2, 5], 1)) == [20]
# assert sorted(sol.k_largest_in_binary_heap([20, 14, 18, 7, 9, 3, 11, 2, 5], 9)) == [2, 3, 5, 7, 9, 11, 14, 18, 20]
# assert sorted(sol.k_largest_in_binary_heap([3, 1], 2)) == [1, 3]
# assert sorted(sol.k_largest_in_binary_heap([10, 1, 9, 0, 0, 8, 7], 3)) == [8, 9, 10]
# assert sorted(sol.k_largest_in_binary_heap([4, 4, 4, 4, 4], 3)) == [4, 4, 4]
# assert sorted(sol.k_largest_in_binary_heap([-1, -5, -2, -9, -6, -3], 4)) == [-5, -3, -2, -1]
# assert sorted(sol.k_largest_in_binary_heap([100, 1, 99, 0, 0, 98, 97, 0, 0, 0, 0, 96, 95], 5)) == [96, 97, 98, 99, 100]
# A = [20, 14, 18, 7, 9, 3, 11, 2, 5]
# assert sorted(sol.k_largest_in_binary_heap(A, 6)) == [7, 9, 11, 14, 18, 20]
# assert A == [20, 14, 18, 7, 9, 3, 11, 2, 5]
# A = list(range(10 ** 5, 0, -1))
# assert sorted(sol.k_largest_in_binary_heap(A, 10)) == list(range(10 ** 5 - 9, 10 ** 5 + 1))
# assert sorted(sol.k_largest_in_binary_heap(A, 10 ** 5)) == list(range(1, 10 ** 5 + 1))
