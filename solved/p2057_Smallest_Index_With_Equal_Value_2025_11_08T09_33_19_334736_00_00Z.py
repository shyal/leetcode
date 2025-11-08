"""
URL: https://leetcode.com/problems/smallest-index-with-equal-value/description/?envType=problem-list-v2&envId=vn57k9wr

2057. Smallest Index With Equal Value

Given a 0-indexed integer array nums, return the smallest index i of nums such that i mod 10 == nums[i], or -1 if such index does not exist.

x mod y denotes the remainder when x is divided by y.

Example 1:

Input: nums = [0,1,2]
Output: 0
Explanation:
i=0: 0 mod 10 = 0 == nums[0].
i=1: 1 mod 10 = 1 == nums[1].
i=2: 2 mod 10 = 2 == nums[2].
All indices have i mod 10 == nums[i], so we return the smallest index 0.

Example 2:

Input: nums = [4,3,2,1]
Output: 2
Explanation:
i=0: 0 mod 10 = 0 != nums[0].
i=1: 1 mod 10 = 1 != nums[1].
i=2: 2 mod 10 = 2 == nums[2].
i=3: 3 mod 10 = 3 != nums[3].
2 is the only index which has i mod 10 == nums[i].

Example 3:

Input: nums = [1,2,3,4,5,6,7,8,9,0]
Output: -1
Explanation: No index satisfies i mod 10 == nums[i].


Constraints:

    1 <= nums.length <= 100
    0 <= nums[i] <= 9
"""


class Solution:
    def smallestEqual(self, nums: List[int]) -> int:
        return next((i for i in range(len(nums)) if i % 10 == nums[i]), -1)


sol = Solution()

# print(sol.smallestEqual([0, 1, 2]))  # 0

assert sol.smallestEqual([0, 1, 2]) == 0
assert sol.smallestEqual([4, 3, 2, 1]) == 2
assert sol.smallestEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) == -1
assert sol.smallestEqual([0]) == 0
assert sol.smallestEqual([1]) == -1
assert sol.smallestEqual([2, 1, 3, 5, 2]) == 1
assert sol.smallestEqual([7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 0]) == 10
# assert sol.smallestEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]) == 9
# assert sol.smallestEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == -1
# assert sol.smallestEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
