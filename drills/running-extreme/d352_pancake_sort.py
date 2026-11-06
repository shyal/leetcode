"""
Given a list of integers arr, sort it ascending and return it. The only
operation that may change arr is flip(k), which reverses the order of
arr[0] through arr[k]. Write flip yourself.

Example 1:

Input: arr = [1, 5, 4, 3, 2]
Output: [1, 2, 3, 4, 5]
Explanation: flip(1) gives [5, 1, 4, 3, 2], then flip(4) gives
[2, 3, 4, 1, 5]: the 5 is in place. Six more flips sort the rest.

Example 2:

Input: arr = [1, 3, 1]
Output: [1, 1, 3]

Example 3:

Input: arr = []
Output: []

Constraints:

    0 <= len(arr) <= 10^3
    -10^9 <= arr[i] <= 10^9

    REQUIRED: O(n^2) time, O(1) extra space, at most 2n flips. NO
    sorted(), NO list.sort(), NO swap of two elements.
"""


class Solution:
    def pancake_sort(self, arr: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.pancake_sort([1, 5, 4, 3, 2]))  # [1, 2, 3, 4, 5]

# assert sol.pancake_sort([1, 5, 4, 3, 2]) == [1, 2, 3, 4, 5]
# assert sol.pancake_sort([1, 3, 1]) == [1, 1, 3]
# assert sol.pancake_sort([]) == []
# assert sol.pancake_sort([1]) == [1]
# assert sol.pancake_sort([1, 2]) == [1, 2]
# assert sol.pancake_sort([2, 1]) == [1, 2]
# assert sol.pancake_sort([3, 1, 2, 4, 6, 5]) == [1, 2, 3, 4, 5, 6]
# assert sol.pancake_sort([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# assert sol.pancake_sort([10, 9, 8, 6, 7, 5, 4, 3, 2, 1, 9, 10, 8, 7, 6, 5, 4, 3, 2, 1, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]
# assert sol.pancake_sort([2, 3, 1, 5, 4]) == [1, 2, 3, 4, 5]
# assert sol.pancake_sort([5, 5, 5]) == [5, 5, 5]
# assert sol.pancake_sort([-1, -3, 2, -2]) == [-3, -2, -1, 2]
# a = [3, 1, 2]
# assert sol.pancake_sort(a) is a and a == [1, 2, 3]
# assert sol.pancake_sort(list(range(1000, 0, -1))) == list(range(1, 1001))
# assert sol.pancake_sort([(i * 7919) % 1000 for i in range(1000)]) == list(range(1000))
