"""
URL: https://leetcode.com/problems/product-of-array-except-self/description/?envType=problem-list-v2&envId=vn57k9wr

238. Product of Array Except Self

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:

    2 <= nums.length <= 10^5
    -30 <= nums[i] <= 30
    The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

---

That old chestnut.


1,        2,        3,        4

2.3.4    1.3.4    1.2.4     1.2.3

1        1.1       1.2     1.2.3
2.3.4   3.4.1      4.1        1


"""


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        left, right = 1, 1
        for i in range(len(nums)):
            res[i] *= left
            res[~i] *= right
            left *= nums[i]
            right *= nums[~i]
        return res


sol = Solution()

print(sol.productExceptSelf([1, 2, 3, 4]))  # [24,12,8,6]

assert sol.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
assert sol.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

assert sol.productExceptSelf([0, 0, 0, 0]) == [0, 0, 0, 0]
assert sol.productExceptSelf([1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1]
assert sol.productExceptSelf([-1, -1, -1, -1]) == [-1, -1, -1, -1]
assert sol.productExceptSelf([30, 30, 30, 30]) == [27000, 27000, 27000, 27000]
assert sol.productExceptSelf([-30, -30, -30, -30]) == [-27000, -27000, -27000, -27000]
assert sol.productExceptSelf([1, -1, 1, -1, 1]) == [1, -1, 1, -1, 1]
assert sol.productExceptSelf([2]) == [1]
assert sol.productExceptSelf([2, 3]) == [3, 2]
assert sol.productExceptSelf([0, 1]) == [1, 0]
assert sol.productExceptSelf([1, 0]) == [0, 1]
assert sol.productExceptSelf([1, 2, 0, 4, 5]) == [0, 0, 40, 0, 0]
