"""
Given a list arr of integers and an integer s, return four elements of
arr, at four different indices, whose sum is s, as a list in ascending
order. If no four elements sum to s, return []. When more than one set
of four sums to s, sort each set and return the one that comes first
when the sorted sets are compared element by element.

Example 1:

Input: arr = [2, 7, 4, 0, 9, 5, 1, 3], s = 20
Output: [0, 4, 7, 9]
Explanation: [1, 3, 7, 9] and [2, 4, 5, 9] also sum to 20. Compared
element by element, [0, 4, 7, 9] comes first.

Example 2:

Input: arr = [4, 4, 4, 4], s = 16
Output: [4, 4, 4, 4]
Explanation: the four indices are different, so one value can appear
four times.

Example 3:

Input: arr = [4, 4, 4, 2], s = 16
Output: []

Constraints:

    1 <= len(arr) <= 100
    -10^4 <= arr[i] <= 10^4
    -10^5 <= s <= 10^5

    REQUIRED: O(n^3) time. NO enumeration of all sets of four indices,
    NO dict or set of pair sums.
"""


class Solution:
    def find_array_quadruplet(self, arr: list[int], s: int) -> list[int]:
        pass


sol = Solution()

print(sol.find_array_quadruplet([2, 7, 4, 0, 9, 5, 1, 3], 20))  # [0, 4, 7, 9]

# assert sol.find_array_quadruplet([2, 7, 4, 0, 9, 5, 1, 3], 20) == [0, 4, 7, 9]
# assert sol.find_array_quadruplet([4, 4, 4, 4], 16) == [4, 4, 4, 4]
# assert sol.find_array_quadruplet([4, 4, 4, 2], 16) == []
# assert sol.find_array_quadruplet([], 12) == []
# assert sol.find_array_quadruplet([4, 4, 4], 12) == []
# assert sol.find_array_quadruplet([2, 7, 4, 0, 9, 5, 1, 3], 120) == []
# assert sol.find_array_quadruplet([1, 2, 3, 4, 5, 9, 19, 12, 12, 19], 40) == [4, 5, 12, 19]
# assert sol.find_array_quadruplet([1, 2, 3, 4], 10) == [1, 2, 3, 4]
# assert sol.find_array_quadruplet([1, 2, 3, 4], 11) == []
# assert sol.find_array_quadruplet([-1, 0, 1, 2, -2], 0) == [-2, -1, 1, 2]
# assert sol.find_array_quadruplet([-10000, 10000, -10000, 10000], 0) == [-10000, -10000, 10000, 10000]
# assert sol.find_array_quadruplet(list(range(100)), 6) == [0, 1, 2, 3]
# assert sol.find_array_quadruplet(list(range(100)), 390) == [96, 97, 98, 99]
# assert sol.find_array_quadruplet(list(range(100)), 391) == []
# assert sol.find_array_quadruplet([7] * 100, 28) == [7, 7, 7, 7]
# assert sol.find_array_quadruplet([7] * 100, 29) == []
