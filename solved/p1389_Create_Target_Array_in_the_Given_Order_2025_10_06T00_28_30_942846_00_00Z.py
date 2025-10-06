"""
URL: https://leetcode.com/problems/create-target-array-in-the-given-order/description/

1389. Create Target Array in the Given Order

Given two arrays of integers nums and index. Your task is to create target array under the following rules:

    Initially target array is empty.
    From left to right read nums[i] and index[i], insert at index index[i] the value nums[i] in target array.
    Repeat the next pair until there are no more to read.

Return the target array.

It is guaranteed that the insertion index is valid.


Example 1:

Input: nums = [0,1,2,3,4], index = [0,1,2,2,1]
Output: [0,4,1,3,2]
Explanation:
nums       index     target
0            0        [0]
1            1        [0,1]
2            2        [0,1,2]
3            2        [0,1,3,2]
4            1        [0,4,1,3,2]

Example 2:

Input: nums = [1,2,3,4,0], index = [0,1,2,3,0]
Output: [0,1,2,3,4]
Explanation:
nums       index     target
1            0        [1]
2            1        [1,2]
3            2        [1,2,3]
4            3        [1,2,3,4]
0            0        [0,1,2,3,4]

Example 3:

Input: nums = [1], index = [0]
Output: [1]


Constraints:

    1 <= nums.length, index.length <= 100
    nums.length == index.length
    0 <= nums[i] <= 100
    0 <= index[i] <= i

"""


class Solution:
    def createTargetArray(self, nums: List[int], index: List[int]) -> List[int]:
        target = []
        for i in range(len(nums)):
            ind = index[i]
            num = nums[i]
            target.insert(ind, num)
        return target


sol = Solution()

assert sol.createTargetArray([0, 1, 2, 3, 4], [0, 1, 2, 2, 1]) == [0, 4, 1, 3, 2]
assert sol.createTargetArray([1, 2, 3, 4, 0], [0, 1, 2, 3, 0]) == [0, 1, 2, 3, 4]
assert sol.createTargetArray([1], [0]) == [1]
assert sol.createTargetArray([1, 2, 3, 4, 5], [0, 0, 0, 0, 0]) == [5, 4, 3, 2, 1]
assert sol.createTargetArray([1, 2, 3], [0, 1, 2]) == [1, 2, 3]
assert sol.createTargetArray([4, 2, 1], [0, 0, 1]) == [2, 1, 4]
assert sol.createTargetArray([0, 0, 0], [0, 0, 0]) == [0, 0, 0]
assert sol.createTargetArray([100, 99, 98], [0, 1, 0]) == [98, 100, 99]
assert sol.createTargetArray([2], [0]) == [2]
