"""
EPI 11.3 Search a cyclically sorted array

Given a cyclically sorted array A of distinct integers, return the
index of its smallest value. An array is cyclically sorted when a
rotation of it is sorted in increasing order: [9, 12, 17, 2, 4, 5] is
the sorted array [2, 4, 5, 9, 12, 17] rotated by three places.

Example 1:

Input: A = [9, 12, 17, 2, 4, 5]
Output: 3

Example 2:

Input: A = [1, 2, 3]
Output: 0

Example 3:

Input: A = [2, 1]
Output: 1

Constraints:

    1 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    The values of A are distinct.

    REQUIRED: O(log n) time, O(1) extra space. NO min(), NO index(),
    NO scan, NO sorting.
"""


class Solution:
    def search_smallest(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.search_smallest([9, 12, 17, 2, 4, 5]))  # 3

# assert sol.search_smallest([9, 12, 17, 2, 4, 5]) == 3
# assert sol.search_smallest([1, 2, 3]) == 0
# assert sol.search_smallest([2, 1]) == 1
# assert sol.search_smallest([7]) == 0
# assert sol.search_smallest([1, 2]) == 0
# assert sol.search_smallest([3, 1, 2]) == 1
# assert sol.search_smallest([2, 3, 1]) == 2
# assert sol.search_smallest([5, 6, 7, 8, 1]) == 4
# assert sol.search_smallest([8, 1, 5, 6, 7]) == 1
# assert sol.search_smallest([4, 5, 6, 7, 0, 1, 2]) == 4
# assert sol.search_smallest([-3, -1, -9, -7, -5]) == 2
# assert sol.search_smallest(list(range(10 ** 5))) == 0
# assert sol.search_smallest(list(range(1, 10 ** 5)) + [0]) == 10 ** 5 - 1
# assert sol.search_smallest([10 ** 5 - 1] + list(range(10 ** 5 - 1))) == 1
# assert sol.search_smallest(list(range(70000, 10 ** 5)) + list(range(70000))) == 30000
