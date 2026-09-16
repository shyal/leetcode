"""
URL: https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

448. Find All Numbers Disappeared in an Array

Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.

Example 1:

Input: nums = [4,3,2,7,8,2,3,1]
Output: [5,6]

Example 2:

Input: nums = [1,1]
Output: [2]

Constraints:

    n == nums.length
    1 <= n <= 10^5
    1 <= nums[i] <= n

Follow up: Could you do it without extra space and in O(n) runtime? You may assume the returned list does not count as extra space.

---


Trying to solve the follow up:

[4, 3, 2, 7, 8, 2, 3, 1]
 0  1  2  3  4  5  6  7

[4, 3, 2, 0, 8, 2, 3, 1]
 0  1  2  3  4  5  6  7

LEETCODE: Accepted (16 ms, 30.4 MB)
"""


class Solution:

    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = []
        nums = set(nums)
        for i in range(1, n + 1):
            if i not in nums:
                res.append(i)
        return res

    def findDisappearedNumbersFollowup(self, nums: List[int]) -> List[int]:
        n = nums[0]
        for _ in nums:
            p = nums[n - 1]
            nums[n - 1] = 0
            n = p

        res = []
        for i, n in enumerate(nums):
            if n:
                res.append(i + 1)
        return res


sol = Solution()

print(sol.findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # [5,6]

assert sol.findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]) == [5, 6]
assert sol.findDisappearedNumbers([1, 1]) == [2]

assert sol.findDisappearedNumbers([1]) == []
assert sol.findDisappearedNumbers([2, 2]) == [1]
assert sol.findDisappearedNumbers([1, 2, 3, 4, 5]) == []
assert sol.findDisappearedNumbers([5, 5, 5, 5, 5]) == [1, 2, 3, 4]
assert sol.findDisappearedNumbers([2, 3, 4, 5, 6, 7, 8, 9, 10, 1]) == []
assert sol.findDisappearedNumbers([10] * 10) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert sol.findDisappearedNumbers(list(range(1, 100001))) == []
