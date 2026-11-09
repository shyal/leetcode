"""
EPI 11.2 Search a sorted array for entry equal to its index

Given a sorted array A of distinct integers, return an index i with
A[i] == i, or -1 when there is no such index. When there are several
such indices, any of them is a correct answer.

Example 1:

Input: A = [-2, 0, 2, 3, 6, 7, 9]
Output: 2 or 3
Explanation: A[2] == 2 and A[3] == 3.

Example 2:

Input: A = [1, 2, 3]
Output: -1

Example 3:

Input: A = [0]
Output: 0

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    A is sorted in increasing order, and its values are distinct.

    REQUIRED: O(log n) time, O(1) extra space. NO scan.
"""


class Solution:
    def search_entry_equal_to_its_index(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.search_entry_equal_to_its_index([-2, 0, 2, 3, 6, 7, 9]))  # 2 or 3

# assert sol.search_entry_equal_to_its_index([-2, 0, 2, 3, 6, 7, 9]) in (2, 3)
# assert sol.search_entry_equal_to_its_index([1, 2, 3]) == -1
# assert sol.search_entry_equal_to_its_index([0]) == 0
# assert sol.search_entry_equal_to_its_index([]) == -1
# assert sol.search_entry_equal_to_its_index([5]) == -1
# assert sol.search_entry_equal_to_its_index([-5]) == -1
# assert sol.search_entry_equal_to_its_index([0, 5]) == 0
# assert sol.search_entry_equal_to_its_index([-1, 1]) == 1
# assert sol.search_entry_equal_to_its_index([-3, -1, 2, 4, 5]) == 2
# assert sol.search_entry_equal_to_its_index([-3, -1, 0, 1, 4]) == 4
# assert sol.search_entry_equal_to_its_index([-3, -1, 1, 4, 6]) == -1
# assert sol.search_entry_equal_to_its_index([0, 1, 2, 3, 4]) in range(5)
# assert sol.search_entry_equal_to_its_index([-10 ** 9, 1, 10 ** 9]) == 1
# assert sol.search_entry_equal_to_its_index(list(range(-5, 10 ** 5 - 5))) == -1
# assert sol.search_entry_equal_to_its_index(list(range(10 ** 5))) in range(10 ** 5)
# assert sol.search_entry_equal_to_its_index([i - 1 for i in range(77777)] + [i + 1 for i in range(77777, 10 ** 5)]) == -1
# assert sol.search_entry_equal_to_its_index([i - 1 for i in range(77777)] + [77777] + [i + 1 for i in range(77778, 10 ** 5)]) == 77777
# assert sol.search_entry_equal_to_its_index([i - 1 for i in range(10 ** 5 - 1)] + [10 ** 5 - 1]) == 10 ** 5 - 1
