"""
DRILL: Next Greater Index (monotonic-stack warm-up for 739)

Given an integer array nums, return an array res of the same length where
res[i] is the INDEX of the first element to the RIGHT of i that is
strictly greater than nums[i]. If no such element exists, res[i] = -1.

Example 1:

Input: nums = [4, 1, 6, 3, 2, 7]
Output: [2, 2, 5, 5, 5, -1]
Explanation:
    nums[0]=4 -> first greater to its right is 6, at index 2
    nums[1]=1 -> first greater to its right is 6, at index 2
    nums[2]=6 -> first greater to its right is 7, at index 5
    nums[3]=3 -> first greater to its right is 7, at index 5
    nums[4]=2 -> first greater to its right is 7, at index 5
    nums[5]=7 -> nothing greater to its right      -> -1

Example 2:

Input: nums = [3, 3, 3]
Output: [-1, -1, -1]
Explanation: "greater" is strict; equal values don't count.

Example 3:

Input: nums = [1, 2, 3]
Output: [1, 2, -1]

Constraints:

    1 <= len(nums) <= 10^5
    -10^9 <= nums[i] <= 10^9

    REQUIRED: one pass, O(n). No nested loops, no scanning ahead.
    Use a plain list as a stack. Hint from your own class: your
    MonotonicStack.push already pops everything the new value beats --
    here, each pop must also WRITE an answer into res before the
    popped item is gone.
"""

from dsa.monotonic_stack import MonotonicStack, Type

class Solution:
    def nextGreaterIndex(self, nums: list[int]) -> list[int]:
        stack = MonotonicStack(Type.decreasing)
        res = [-1] * len(nums)
        for i, v in enumerate(nums):
            for _, tag in stack.push((v, i)):
                res[tag] = i
        return res
        

sol = Solution()

print(sol.nextGreaterIndex([4, 1, 6, 3, 2, 7])) # [2, 2, 5, 5, 5, -1]

assert sol.nextGreaterIndex([4, 1, 6, 3, 2, 7]) == [2, 2, 5, 5, 5, -1]
assert sol.nextGreaterIndex([3, 3, 3]) == [-1, -1, -1]
assert sol.nextGreaterIndex([1, 2, 3]) == [1, 2, -1]
assert sol.nextGreaterIndex([3, 2, 1]) == [-1, -1, -1]
assert sol.nextGreaterIndex([5]) == [-1]
assert sol.nextGreaterIndex([2, 1, 2]) == [-1, 2, -1]
assert sol.nextGreaterIndex([1, 3, 1, 3]) == [1, -1, 3, -1]
assert sol.nextGreaterIndex([10, 1, 2, 3]) == [-1, 2, 3, -1]

print("All tests passed!")
