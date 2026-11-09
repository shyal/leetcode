"""
EPI 12.9 Find the length of a longest contained interval

Given a list of integers A, return the size of the largest set of
consecutive integers x, x + 1, ..., y such that every integer of the
set is in A. The list A is not sorted and can hold duplicates. The
empty list gives 0.

Example 1:

Input: A = [8, 1, 9, 3, 10, 2, 11]
Output: 4
Explanation: 8, 9, 10 and 11 are all in A. The integers 1, 2 and 3 give
a set of size 3.

Example 2:

Input: A = [5, 7, 9]
Output: 1

Example 3:

Input: A = [2, 2, 3]
Output: 2
Explanation: the duplicate 2 counts once.

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(n) time, where n is the length of A. NO sorting.
"""


class Solution:
    def longest_contained_range(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.longest_contained_range([8, 1, 9, 3, 10, 2, 11]))  # 4

# assert sol.longest_contained_range([8, 1, 9, 3, 10, 2, 11]) == 4
# assert sol.longest_contained_range([5, 7, 9]) == 1
# assert sol.longest_contained_range([2, 2, 3]) == 2
# assert sol.longest_contained_range([]) == 0
# assert sol.longest_contained_range([5]) == 1
# assert sol.longest_contained_range([5, 5]) == 1
# assert sol.longest_contained_range([-3, -1, -2]) == 3
# assert sol.longest_contained_range([0, -1, 1]) == 3
# assert sol.longest_contained_range([1, 3, 5, 2, 4]) == 5
# assert sol.longest_contained_range([1, 2, 2, 3, 3, 3]) == 3
# assert sol.longest_contained_range([10, 1, 2, 20, 21, 22, 23]) == 4
# assert sol.longest_contained_range([10 ** 9, -10 ** 9]) == 1
# assert sol.longest_contained_range(list(range(10 ** 5, 0, -1))) == 10 ** 5
# assert sol.longest_contained_range(list(range(0, 2 * 10 ** 5, 2))) == 1
# assert sol.longest_contained_range(list(range(0, 10 ** 5, 2)) + list(range(1, 10 ** 5, 2))) == 10 ** 5
