"""
URL: https://leetcode.com/problems/rearrange-array-to-maximize-prefix-score/description/?envType=problem-list-v2&envId=vn57k9wr

2587. Rearrange Array to Maximize Prefix Score

You are given a 0-indexed integer array nums. You can rearrange the elements of nums to any order (including the given order).

Let prefix be the array containing the prefix sums of nums after rearranging it. In other words, prefix[i] is the sum of the elements from 0 to i in nums after rearranging it. The score of nums is the number of positive integers in the array prefix.

Return the maximum score you can achieve.

Example 1:

Input: nums = [2,-1,0,1,-3,3,-3]
Output: 6
Explanation: We can rearrange the array into nums = [2,3,1,-1,-3,0,-3].
prefix = [2,5,6,5,2,2,-1], so the score is 6.
It can be shown that 6 is the maximum score we can obtain.

Example 2:

Input: nums = [-2,-3,0]
Output: 0
Explanation: Any rearrangement of the array will result in a score of 0.

Constraints:

    1 <= nums.length <= 10^5
    -10^6 <= nums[i] <= 10^6

---

LEETCODE: Accepted (95 ms, 32.3 MB)
"""


class Solution:
    def maxScore(self, nums: List[int]) -> int:
        def score(arr):
            return sum(1 for x in arr if x >= 1)

        def prefix(arr):
            return [*accumulate(arr)]

        nums.sort(reverse=True)
        p = prefix(nums)
        return score(p)


sol = Solution()

print(sol.maxScore([2, -1, 0, 1, -3, 3, -3]))  # 6

assert sol.maxScore([2, -1, 0, 1, -3, 3, -3]) == 6
assert sol.maxScore([-2, -3, 0]) == 0

assert sol.maxScore([10**6, -(10**6), 1, -1, 0]) == 4
assert sol.maxScore([0]) == 0
assert sol.maxScore([-1]) == 0
assert sol.maxScore([1]) == 1
assert sol.maxScore([1, 1, 1, 1, 1]) == 5
assert sol.maxScore([-1, -1, -1, -1, -1]) == 0
assert sol.maxScore([10**6] * 10**5) == 100000
assert sol.maxScore([-(10**6)] * 10**5) == 0
assert sol.maxScore([0] * 10**5) == 0
assert sol.maxScore([1, -1] * 50000) == 99999
assert sol.maxScore([10**6, 10**6, -(10**6), -(10**6), 0, 0]) == 5
assert sol.maxScore([5, 5, 5, -10, -10, -10]) == 4
