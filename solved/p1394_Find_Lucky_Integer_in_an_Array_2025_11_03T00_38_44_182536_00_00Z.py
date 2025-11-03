"""
URL: https://leetcode.com/problems/find-lucky-integer-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

1394. Find Lucky Integer in an Array

Given an array of integers arr, a lucky integer is an integer that has a frequency in the array equal to its value.

Return the largest lucky integer in the array. If there is no lucky integer return -1.

Example 1:

Input: arr = [2,2,3,4]
Output: 2
Explanation: The only lucky number in the array is 2 because frequency[2] == 2.

Example 2:

Input: arr = [1,2,2,3,3,3]
Output: 3
Explanation: 1, 2 and 3 are all lucky numbers, return the largest of them.

Example 3:

Input: arr = [2,2,2,3,3]
Output: -1
Explanation: There are no lucky numbers in the array.

Constraints:

    1 <= arr.length <= 500
    1 <= arr[i] <= 500
"""


class Solution:
    def findLucky(self, arr: List[int]) -> int:
        return next(
            iter(
                [
                    val
                    for val, count in sorted(Counter(arr).items(), reverse=True)
                    if val == count
                ]
            ),
            -1,
        )


sol = Solution()

assert sol.findLucky([2, 2, 3, 4]) == 2
assert sol.findLucky([1, 2, 2, 3, 3, 3]) == 3
assert sol.findLucky([2, 2, 2, 3, 3]) == -1
assert sol.findLucky([1]) == 1
assert sol.findLucky([1, 1]) == -1
assert sol.findLucky([2]) == -1
assert sol.findLucky([2, 2]) == 2
assert sol.findLucky([1, 2, 3, 4, 5]) == 1
assert sol.findLucky([2, 3, 4, 5]) == -1
assert sol.findLucky([5, 5, 5, 5, 5]) == 5
assert sol.findLucky([5, 5, 5, 5]) == -1
assert sol.findLucky([1, 1, 2, 2]) == 2
assert sol.findLucky([1, 5, 5, 5, 5, 5]) == 5
assert sol.findLucky([3, 3, 3, 4, 4, 4, 4]) == 4
assert sol.findLucky([500] * 500) == 500
