"""
EPI 11.1 Search a sorted array for first occurrence of k

Given an array A sorted in nondecreasing order and an integer k, return
the smallest index i with A[i] == k, or -1 when k is not in A.

Example 1:

Input: A = [1, 3, 3, 3, 5, 8], k = 3
Output: 1

Example 2:

Input: A = [1, 3, 3, 3, 5, 8], k = 4
Output: -1

Example 3:

Input: A = [2, 2, 2], k = 2
Output: 0

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i], k <= 10^9
    A is sorted in nondecreasing order.

    REQUIRED: O(log n) time, O(1) extra space. NO bisect, NO index(),
    NO scan.
"""


class Solution:
    def search_first_of_k(self, A: list[int], k: int) -> int:
        pass


sol = Solution()

print(sol.search_first_of_k([1, 3, 3, 3, 5, 8], 3))  # 1

# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 3) == 1
# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 4) == -1
# assert sol.search_first_of_k([2, 2, 2], 2) == 0
# assert sol.search_first_of_k([], 1) == -1
# assert sol.search_first_of_k([5], 5) == 0
# assert sol.search_first_of_k([5], 4) == -1
# assert sol.search_first_of_k([5], 6) == -1
# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 1) == 0
# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 8) == 5
# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 0) == -1
# assert sol.search_first_of_k([1, 3, 3, 3, 5, 8], 9) == -1
# assert sol.search_first_of_k([1, 2, 2, 9, 9], 9) == 3
# assert sol.search_first_of_k([-10 ** 9, 10 ** 9], 10 ** 9) == 1
# assert sol.search_first_of_k([0] * 10 ** 5, 0) == 0
# assert sol.search_first_of_k([0] * (10 ** 5 - 1) + [1], 1) == 10 ** 5 - 1
# assert sol.search_first_of_k([v // 7 for v in range(10 ** 5)], 9999) == 69993
# assert sol.search_first_of_k(list(range(0, 2 * 10 ** 5, 2)), 99999) == -1
