"""
https://leetcode.com/problems/shuffle-the-array/

1470. Shuffle the Array
Easy
Given the array nums consisting of 2n elements in the form [x1,x2,...,xn,y1,y2,...,yn].

Return the array in the form [x1,y1,x2,y2,...,xn,yn].

Example 1:

Input: nums = [2,5,1,3,4,7], n = 3
Output: [2,3,5,4,1,7] 
Explanation: Since x1=2, x2=5, x3=1, y1=3, y2=4, y3=7 then the answer is [2,3,5,4,1,7].
Example 2:

Input: nums = [1,2,3,4,4,3,2,1], n = 4
Output: [1,4,2,3,3,2,4,1]
Example 3:

Input: nums = [1,1,2,2], n = 2
Output: [1,2,1,2]
 

Constraints:

1 <= n <= 500
nums.length == 2n
1 <= nums[i] <= 10^3
"""

from itertools import chain


class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        return [*chain(*[[nums[i], nums[n + i]] for i in range(n)])]


sol = Solution()
assert sol.shuffle(nums=[2, 5, 1, 3, 4, 7], n=3) == [2, 3, 5, 4, 1, 7]
assert sol.shuffle(nums=[1, 2, 3, 4, 4, 3, 2, 1], n=4) == [1, 4, 2, 3, 3, 2, 4, 1]
assert sol.shuffle(nums=[1, 1, 2, 2], n=2) == [1, 2, 1, 2]
assert sol.shuffle(nums=[1, 2], n=1) == [1, 2]
assert sol.shuffle(nums=[5, 6], n=1) == [5, 6]
assert sol.shuffle(nums=[1, 3, 5, 7, 2, 4, 6, 8], n=4) == [1, 2, 3, 4, 5, 6, 7, 8]
assert sol.shuffle(nums=[10, 20, 30, 40, 50, 60], n=3) == [10, 40, 20, 50, 30, 60]
assert sol.shuffle(nums=[100, 200], n=1) == [100, 200]
assert sol.shuffle(nums=[1, 1, 1, 1, 1, 1], n=3) == [1, 1, 1, 1, 1, 1]
assert sol.shuffle(nums=[2, 4, 6, 8, 10, 12, 1, 3, 5, 7, 9, 11], n=6) == [
    2,
    1,
    4,
    3,
    6,
    5,
    8,
    7,
    10,
    9,
    12,
    11,
]
assert sol.shuffle(nums=[999, 1000, 1, 2], n=2) == [999, 1, 1000, 2]
assert sol.shuffle(nums=[3, 6, 9, 12, 15, 18, 21, 24, 1, 2, 3, 4, 5, 6, 7, 8], n=8) == [
    3,
    1,
    6,
    2,
    9,
    3,
    12,
    4,
    15,
    5,
    18,
    6,
    21,
    7,
    24,
    8,
]
assert sol.shuffle(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], n=5) == [
    1,
    6,
    2,
    7,
    3,
    8,
    4,
    9,
    5,
    10,
]
assert sol.shuffle(nums=[50, 51, 52, 53], n=2) == [50, 52, 51, 53]
assert sol.shuffle(nums=[1000, 999, 998, 1, 2, 3], n=3) == [1000, 1, 999, 2, 998, 3]
assert sol.shuffle(nums=[7, 14], n=1) == [7, 14]

