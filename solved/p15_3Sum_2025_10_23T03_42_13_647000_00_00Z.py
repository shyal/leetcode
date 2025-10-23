"""
URL: https://leetcode.com/problems/3sum/description/

15. 3Sum

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.


Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.


Constraints:

    3 <= nums.length <= 3000
    -105 <= nums[i] <= 105

---

Still managed to come short... `seen` needs to be inside the inner loop.

This is frustrating.

Keeping on the learning stack.

"""


class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set()
        for i in range(len(nums)):
            seen = set()
            target = -nums[i]
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in seen:
                    res.add(tuple(sorted([nums[i], nums[j], complement])))
                seen.add(nums[j])
        return [list(x) for x in res]


sol = Solution()
# assert sol.threeSum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
# assert sol.threeSum([0, 1, 1]) == []
# assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]
# assert sol.threeSum([1, 2, -3]) == [[-3, 1, 2]]
# assert sol.threeSum([-2, 0, 2]) == [[-2, 0, 2]]
# assert sol.threeSum([0, 0, 1]) == []
# assert sol.threeSum([-1, 1, 0]) == [[-1, 0, 1]]
# assert sol.threeSum([1, 1, 1]) == []
# assert sol.threeSum([-4, -2, -2, -2, 0, 1, 2, 2, 4]) == [
#     [-4, 2, 2],
#     [-2, 0, 2],
#     [-4, 0, 4],
#     [-2, -2, 4],
# ]
# assert sol.threeSum([3, 3, -3, -3, -6, -6]) == [[-6, 3, 3]]
# assert sol.threeSum([100000, -50000, -50000]) == [[-50000, -50000, 100000]]
# assert sol.threeSum([1, -1, 3]) == []
# assert sol.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
# assert sol.threeSum([-1, -2, -3]) == []
# assert sol.threeSum([-1, -1, -1, 1, 1, 1]) == []
