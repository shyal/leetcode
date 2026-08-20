"""
URL: https://leetcode.com/problems/running-sum-of-1d-array/description/?envType=problem-list-v2&envId=vn57k9wr

1480. Running Sum of 1d Array

Given an array nums. We define a running sum of an array as
runningSum[i] = sum(nums[0]...nums[i]).

Return the running sum of nums.


Example 1:

Input: nums = [1,2,3,4]
Output: [1,3,6,10]
Explanation: Running sum is obtained as follows: [1, 1+2, 1+2+3, 1+2+3+4].

Example 2:

Input: nums = [1,1,1,1,1]
Output: [1,2,3,4,5]
Explanation: Running sum is obtained as follows: [1, 1+1, 1+1+1, 1+1+1+1, 1+1+1+1+1].

Example 3:

Input: nums = [3,1,2,10,1]
Output: [3,4,6,16,17]


Constraints:

    1 <= nums.length <= 1000
    -10^6 <= nums[i] <= 10^6
"""


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        prefix = 0
        res = []
        for n in nums:
            prefix += n
            res.append(prefix)
        return res


sol = Solution()

# print(sol.runningSum([1, 2, 3, 4]))  # [1, 3, 6, 10]

assert sol.runningSum([1, 2, 3, 4]) == [1, 3, 6, 10]
assert sol.runningSum([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]
assert sol.runningSum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]
assert sol.runningSum([5]) == [5]
assert sol.runningSum([0]) == [0]
assert sol.runningSum([-5]) == [-5]
assert sol.runningSum([]) == []
assert sol.runningSum([0, 0, 0, 0]) == [0, 0, 0, 0]
assert sol.runningSum([-1, -2, -3, -4]) == [-1, -3, -6, -10]
assert sol.runningSum([1, -1, 1, -1]) == [1, 0, 1, 0]
assert sol.runningSum([-3, 3, -3, 3]) == [-3, 0, -3, 0]
assert sol.runningSum([10**6, 10**6, 10**6]) == [1000000, 2000000, 3000000]
assert sol.runningSum([-(10**6), -(10**6), -(10**6)]) == [-1000000, -2000000, -3000000]
assert sol.runningSum([10**6, -(10**6)]) == [1000000, 0]
assert sol.runningSum([-(10**6), 10**6, 10**6]) == [-1000000, 0, 1000000]
assert sol.runningSum([0, 5, 0, -5, 0]) == [0, 5, 5, 0, 0]
assert sol.runningSum([2, 0, 2, 0, 2]) == [2, 2, 4, 4, 6]
assert sol.runningSum([1] * 1000) == list(range(1, 1001))
assert sol.runningSum([10**6] * 1000)[-1] == 10**9
assert sol.runningSum([-(10**6)] * 1000)[0] == -(10**6)
assert len(sol.runningSum([7] * 1000)) == 1000
assert sol.runningSum(list(range(1, 11))) == [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]

_orig = [1, 2, 3, 4]
_res = sol.runningSum(_orig)
assert _orig == [1, 2, 3, 4]
assert _res is not _orig
