"""
URL: https://leetcode.com/problems/peak-index-in-a-mountain-array/description/

852. Peak Index in a Mountain Array

An array arr is a mountain if it satisfies the following conditions:

    arr.length >= 3
    There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
        arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
        arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

Given a mountain array arr, return the index i such that it is the peak of the mountain array.

You must solve it in O(log(arr.length)) time complexity.


Example 1:

Input: arr = [0,1,0]
Output: 1

Example 2:

Input: arr = [0,2,1,0]
Output: 1

Example 3:

Input: arr = [0,10,5,2]
Output: 1


Constraints:

    3 <= arr.length <= 10^5
    0 <= arr[i] <= 10^6
    arr is guaranteed to be a mountain array.
"""


class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        left, right = 1, len(arr) - 2
        while left <= right:
            mid = (left + right) // 2
            if arr[mid - 1] < arr[mid] > arr[mid + 1]:
                return mid
            elif arr[mid - 1] > arr[mid]:
                right = mid - 1
            else:
                left = mid + 1


sol = Solution()

# print(sol.peakIndexInMountainArray([0, 1, 0]))  # 1

assert sol.peakIndexInMountainArray([0, 1, 0]) == 1
assert sol.peakIndexInMountainArray([0, 2, 1, 0]) == 1
assert sol.peakIndexInMountainArray([0, 10, 5, 2]) == 1
assert sol.peakIndexInMountainArray([1, 2, 3, 1]) == 2
assert sol.peakIndexInMountainArray([1, 2, 3, 4, 3, 2, 1]) == 3
assert sol.peakIndexInMountainArray([5, 6, 7, 8, 9, 10, 9]) == 5
assert (
    sol.peakIndexInMountainArray(
        [10, 20, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    )
    == 1
)
assert sol.peakIndexInMountainArray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9]) == 9
assert sol.peakIndexInMountainArray([3, 4, 5, 1]) == 2
assert sol.peakIndexInMountainArray([24, 69, 100, 99, 79, 78, 67, 36, 26, 19]) == 2
