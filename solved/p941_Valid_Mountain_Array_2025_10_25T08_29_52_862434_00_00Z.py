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

Tried to use binary search, however it seems this can't be done
faster than O(n).

Saw a discussion about using max.., then effectively two pointers
outwards from there. Seems good but not as optimal as can be.

The most optimal is to check for strictly increasing, then we no longer
strictly increasing start expecting strictly decreasing.

"""


class Solution:

    def validMountainArray(self, arr: List[int]) -> bool:
        n = len(arr)
        if n < 3:
            return False

        peak_from_left = None

        for i, v in enumerate(arr):
            if i == 0 or (i > 0 and arr[i - 1] < arr[i]):
                peak_from_left = i, v
            else:
                break

        for i in range(len(arr) - 1, -1, -1):
            if i == n - 1 or (i < n - 1 and arr[i] > arr[i + 1]):
                peak_from_right = i, arr[i]
            else:
                break

        return (
            peak_from_left == peak_from_right
            and peak_from_left[0] != n - 1
            and peak_from_right[0] != 0
        )


sol = Solution()

assert sol.validMountainArray([2, 1]) == False
assert sol.validMountainArray([3, 5, 5]) == False
assert sol.validMountainArray([0, 3, 2, 1]) == True
assert sol.validMountainArray([0]) == False
assert sol.validMountainArray([1, 2]) == False
assert sol.validMountainArray([2, 1, 0]) == False
assert sol.validMountainArray([0, 1, 2]) == False
assert sol.validMountainArray([0, 1, 0]) == True
assert sol.validMountainArray([1, 3, 2, 4]) == False
assert sol.validMountainArray([1, 2, 3, 2, 1]) == True
assert sol.validMountainArray([3, 5, 5, 4]) == False
assert sol.validMountainArray([0, 2, 3, 4, 3, 2, 1]) == True
assert sol.validMountainArray([0, 2, 3, 3, 4, 3, 2, 1]) == False
assert sol.validMountainArray([0, 2, 3, 4, 3, 3, 2, 1]) == False
assert sol.validMountainArray([1, 1, 1]) == False
assert sol.validMountainArray([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]) == False
assert sol.validMountainArray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == False
