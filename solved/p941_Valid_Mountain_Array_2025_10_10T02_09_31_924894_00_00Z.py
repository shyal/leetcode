"""
URL: https://leetcode.com/problems/valid-mountain-array/description/

941. Valid Mountain Array

Given an integer array arr, return true if and only if it is a valid mountain array.

Recall that arr is a mountain array if and only if:

    arr.length >= 3
    There exists some i with 0 < i < arr.length - 1 such that:
        arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
        arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

Example 1:

Input: arr = [2,1]
Output: false

Example 2:

Input: arr = [3,5,5]
Output: false

Example 3:

Input: arr = [0,3,2,1]
Output: true

Constraints:

    1 <= arr.length <= 10^4
    0 <= arr[i] <= 10^4

---

941 is not an easy question. Easy tag is misleading,
so not great being told something is easy when it isn't.

Will revisit with the medium framing.

"""

from typing import List


class Solution:
    def validMountainArray(self, arr: List[int]) -> bool:
        is_increasing = lambda i: arr[i - 1] < arr[i]
        is_decreasing = lambda i: arr[i - 1] > arr[i]
        is_peak = (
            lambda i: i > 0
            and is_increasing(i - 1)
            and (is_decreasing(i + 1))
            and i < len(arr)
        )

        # for i in range(1, len(arr) - 1):
        #     print(i)
        #     print(f"increasing: {is_increasing(i)}")
        #     print(f"peak: {is_peak(i)}")
        #     print(f"decreasing: {is_decreasing(i)}")
        #     print("------")


sol = Solution()

# print(sol.validMountainArray([2, 1, 0]))  # False

# assert sol.validMountainArray([2, 1]) == False
# assert sol.validMountainArray([3, 5, 5]) == False
# assert sol.validMountainArray([0, 3, 2, 1]) == True
# assert sol.validMountainArray([0]) == False
# assert sol.validMountainArray([1, 2]) == False
# # assert sol.validMountainArray([2, 1, 0]) == False
# assert sol.validMountainArray([0, 1, 2]) == False
# # assert sol.validMountainArray([0, 1, 0]) == True
# assert sol.validMountainArray([1, 3, 2, 4]) == False
# assert sol.validMountainArray([1, 2, 3, 2, 1]) == True
# # assert sol.validMountainArray([3, 5, 5, 4]) == False
# assert sol.validMountainArray([0, 2, 3, 4, 3, 2, 1]) == True
# assert sol.validMountainArray([0, 2, 3, 3, 4, 3, 2, 1]) == False
# assert sol.validMountainArray([0, 2, 3, 4, 3, 3, 2, 1]) == False
# assert sol.validMountainArray([1, 1, 1]) == False
# # assert sol.validMountainArray([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]) == False
# assert sol.validMountainArray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == False
