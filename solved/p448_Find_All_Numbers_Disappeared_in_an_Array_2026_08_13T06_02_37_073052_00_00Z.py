"""
URL: https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

448. Find All Numbers Disappeared in an Array

Given an array nums of n integers where nums[i] is in the range [1, n], return
an array of all the integers in the range [1, n] that do not appear in nums.


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


Follow up: Could you do it without extra space and in O(n) runtime? You may
assume the returned list does not count as extra space.

---

Hoping this is considered a canonical solve for the generate-and-test-neighbours node.
"""

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        S = set(nums)
        res = []
        for n in range(1, len(nums) + 1):
            if n not in S:
                res.append(n)
        return res


sol = Solution()

# print(sol.findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # [5, 6]

assert sol.findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]) == [5, 6]
assert sol.findDisappearedNumbers([1, 1]) == [2]
assert sol.findDisappearedNumbers([1]) == []
assert sol.findDisappearedNumbers([2, 2]) == [1]
assert sol.findDisappearedNumbers([1, 2]) == []
assert sol.findDisappearedNumbers([2, 1]) == []
assert sol.findDisappearedNumbers([3, 3, 3]) == [1, 2]
assert sol.findDisappearedNumbers([1, 1, 1, 1]) == [2, 3, 4]
assert sol.findDisappearedNumbers([4, 4, 4, 4]) == [1, 2, 3]
assert sol.findDisappearedNumbers([2, 2, 2, 2]) == [1, 3, 4]
assert sol.findDisappearedNumbers([5, 4, 3, 2, 1]) == []
assert sol.findDisappearedNumbers([1, 2, 2, 4]) == [3]
assert sol.findDisappearedNumbers([2, 3, 1, 5, 5]) == [4]
assert sol.findDisappearedNumbers([10, 2, 5, 10, 9, 1, 1, 4, 3, 7]) == [6, 8]
assert sol.findDisappearedNumbers(list(range(1, 101))) == []
assert sol.findDisappearedNumbers([1] * 100) == list(range(2, 101))