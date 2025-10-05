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

Ok since we need the indices, i'm thinking of using the hash map approach, so
first build the two sums variant, then use two sum for three sum.

We need to track all occurrances of two sum, so use a defaultdict of set.

So my solution works, but has a TLE with long input.

I botched this one... because i didn't notice the requirements was for unique
values rather than unique indices.

I'd rather revisit it later.
"""


class Solution:

    def twoSum(self, nums, target=0, exclude=-1):
        D, indices = dd(set), []
        for i, n in enumerate(nums):
            if i == exclude:
                continue
            comp = target - n
            if comp in D:
                matches = [
                    ((j, i) if i > j else (j, i)) for j in D[comp] if j != exclude
                ]
                if matches:
                    indices.extend(matches)
            D[n].add(i)
        return indices

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set([])
        for i, n in enumerate(nums):
            for ts in self.twoSum(nums, -n, i):
                res.add(tuple(sorted([nums[i], nums[ts[0]], nums[ts[1]]])))
        return list(list(x) for x in res)[::-1]


sol = Solution()

# TLE = [0] * 3000
# assert sol.threeSum(TLE) == [[0, 0, 0]]
assert sol.threeSum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert sol.threeSum([0, 1, 1]) == []
assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]
assert sol.threeSum([1, 2, -3]) == [[-3, 1, 2]]
assert sol.threeSum([-2, 0, 2]) == [[-2, 0, 2]]
assert sol.threeSum([0, 0, 1]) == []
assert sol.threeSum([-1, 1, 0]) == [[-1, 0, 1]]
assert sol.threeSum([1, 1, 1]) == []
assert sol.threeSum([-4, -2, -2, -2, 0, 1, 2, 2, 4]) == [
    [-4, 2, 2],
    [-2, 0, 2],
    [-4, 0, 4],
    [-2, -2, 4],
]
assert sol.threeSum([3, 3, -3, -3, -6, -6]) == [[-6, 3, 3]]
assert sol.threeSum([100000, -50000, -50000]) == [[-50000, -50000, 100000]]
assert sol.threeSum([1, -1, 3]) == []
assert sol.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
assert sol.threeSum([-1, -2, -3]) == []
assert sol.threeSum([-1, -1, -1, 1, 1, 1]) == []
