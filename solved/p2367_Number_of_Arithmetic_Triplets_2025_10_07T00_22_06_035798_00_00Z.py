"""
URL: https://leetcode.com/problems/number-of-arithmetic-triplets/description/?envType=study-plan-v2&envId=leetcode-75

2367. Number of Arithmetic Triplets

You are given a 0-indexed, strictly increasing integer array nums and a positive integer diff. A triplet (i, j, k) is an arithmetic triplet if the following conditions are met:

- i < j < k,
- nums[j] - nums[i] == diff, and
- nums[k] - nums[j] == diff.

Return the number of unique arithmetic triplets.


Example 1:

Input: nums = [0,1,4,6,7,10], diff = 3
Output: 2
Explanation:
(1, 2, 4) is an arithmetic triplet because both 4 - 1 == 3 and 7 - 4 == 3.
(2, 4, 5) is an arithmetic triplet because both 7 - 4 == 3 and 10 - 7 == 3.

Example 2:

Input: nums = [4,5,6,7,8,9], diff = 2
Output: 2
Explanation:
(0, 2, 4) is an arithmetic triplet because both 6 - 4 == 2 and 8 - 6 == 2.
(1, 3, 5) is an arithmetic triplet because both 7 - 5 == 2 and 9 - 7 == 2.


Constraints:

    3 <= nums.length <= 200
    0 <= nums[i] <= 200
    1 <= diff <= 50
    nums is strictly increasing.
"""


class Solution:
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        triplets = 0
        for i, j, k in combinations(range(len(nums)), 3):
            if nums[j] - nums[i] == diff and nums[k] - nums[j] == diff:
                triplets += 1
        return triplets


sol = Solution()

assert sol.arithmeticTriplets([0, 1, 4, 6, 7, 10], 3) == 2
assert sol.arithmeticTriplets([4, 5, 6, 7, 8, 9], 2) == 2
assert sol.arithmeticTriplets([0, 1, 2], 1) == 1
assert sol.arithmeticTriplets([0, 1, 3], 1) == 0
assert sol.arithmeticTriplets([1, 3, 5, 7, 9], 2) == 3
assert sol.arithmeticTriplets([0, 2, 4, 6], 2) == 2
assert sol.arithmeticTriplets([0, 50, 100], 50) == 1
assert sol.arithmeticTriplets([100, 150, 200], 50) == 1
assert sol.arithmeticTriplets([0, 1, 2], 2) == 0
assert sol.arithmeticTriplets([1, 2, 3, 4, 5, 6], 1) == 4
assert sol.arithmeticTriplets([0, 10, 20, 30, 50], 5) == 0
