# URL: https://leetcode.com/problems/next-greater-element-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 503. Next Greater Element II
#
# Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.
#
# The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.
#
# Example 1:
#
# Input: nums = [1,2,1]
# Output: [2,-1,2]
# Explanation: The first 1's next greater number is 2;
# The number 2 can't find next greater number.
# The second 1's next greater number needs to search circularly, which is also 2.
#
# Example 2:
#
# Input: nums = [1,2,3,4,3]
# Output: [2,3,4,-1,4]
#
# Constraints:
#
#     1 <= nums.length <= 10^4
#     -10^9 <= nums[i] <= 10^9
#
# ---
# 
# [1, 3, 2, 4, 3, 5]
# [3, 4, 4, 5, 5, -1]
# 
# LEETCODE: Accepted (54 ms, 21.6 MB)

# mu 0.12

from operator import gt, lt


class StackType
    decreasing = 0
    increasing = 1


class MonotonicStack

    def __init__(type)
        self.data = []
        self.type = type

    def push(val)
        op = (lt, gt)[self.type]
        res = []
        while self.data and op(self.data[-1][0], val[0])
            res.append(self.data.pop())
        self.data.append(val)
        return res

    def pop()
        if self.data
            return self.data.pop()

    def peek()
        if self.data
            return self.data[-1]

    def __str__()
        return str(self.data)


class Solution
  def nextGreaterElements(nums: [int]) -> [int]
    s = MonotonicStack(0)
    n = len nums
    res = table(len(nums), fill=-1)
    for >i, v in nums + nums
      for vv, ii in s.push((v, i))
        res[ii % n] = v
    res[:n]

sol = Solution()

# print(sol.nextGreaterElements([5, 4, 3, 2, 1]))# == [-1, 5, 5, 5, 5]

# print(sol.nextGreaterElements([1, 2, 1]))  # [2,-1,2]

assert sol.nextGreaterElements([1, 2, 1]) == [2, -1, 2]
assert sol.nextGreaterElements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
assert sol.nextGreaterElements([1]) == [-1]
assert sol.nextGreaterElements([2, 2, 2, 2]) == [-1, -1, -1, -1]
assert sol.nextGreaterElements([-1, -2, -3, -4]) == [-1, -1, -1, -1]
assert sol.nextGreaterElements([5, 4, 3, 2, 1]) == [-1, 5, 5, 5, 5]
assert sol.nextGreaterElements([1, 3, 2, 4, 3, 5]) == [3, 4, 4, 5, 5, -1]
assert sol.nextGreaterElements([10 ** 9, -10 ** 9, 0, 10 ** 8]) == [-1, 0, 100000000, 1000000000]
assert sol.nextGreaterElements([1, 1, 1, 2, 2, 2, 3, 3, 3]) == [2, 2, 2, 3, 3, 3, -1, -1, -1]
assert sol.nextGreaterElements([3, 1, 3, 1, 3]) == [-1, 3, -1, 3, -1]
assert sol.nextGreaterElements([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [2, 3, 4, 5, 6, 7, 8, 9, 10, -1]
