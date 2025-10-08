"""
URL: https://leetcode.com/problems/minimum-size-subarray-sum/description/

209. Minimum Size Subarray Sum

Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

Example 1:

Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: The subarray [4,3] has the minimal length under the problem constraint.

Example 2:

Input: target = 4, nums = [1,4,4]
Output: 1

Example 3:

Input: target = 11, nums = [1,1,1,1,1,1,1,1]
Output: 0

Constraints:

    1 <= target <= 10^9
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^4

---

Let's begin with subarray sum equals k. I was very close to remembering it
Useful warmup.

Now to this problem. It seems the main thing that might help here is the
ability to get the sum between i and j, which we can do with a prefix array.

Then a sliding window which grows and shrinks to find subarrays gte to the target.
Then track the min size of the window.

Solved.
"""


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        prefix = [*accumulate(nums)] + [0]
        range_sum = lambda i, j: prefix[j] - prefix[i - 1]
        i, j = 0, 0
        min_size = float("inf")
        while j < len(nums):
            _sum = range_sum(i, j)
            if _sum < target:
                j += 1
            elif _sum > target:
                min_size = min(min_size, j - i + 1)
                i += 1
            else:
                min_size = min(min_size, j - i + 1)
                i += 1
        return min_size if min_size != float("inf") else 0


sol = Solution()

# print(sol.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]))  # 2

assert sol.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
assert sol.minSubArrayLen(4, [1, 4, 4]) == 1
assert sol.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
assert sol.minSubArrayLen(1, [1]) == 1
assert sol.minSubArrayLen(1, [2]) == 1
assert sol.minSubArrayLen(3, [1]) == 0
assert sol.minSubArrayLen(5, [1, 1, 1, 1, 1]) == 5
assert sol.minSubArrayLen(6, [1, 1, 1, 1, 1]) == 0
assert sol.minSubArrayLen(15, [1, 2, 3, 4, 5, 6]) == 3
assert sol.minSubArrayLen(3, [1, 2, 3]) == 1
assert sol.minSubArrayLen(5, [1, 2, 3]) == 2
assert sol.minSubArrayLen(4, [1, 4, 1]) == 1
assert sol.minSubArrayLen(4, [4, 1, 1]) == 1
assert sol.minSubArrayLen(4, [1, 1, 4]) == 1
assert sol.minSubArrayLen(10, [5, 5]) == 2
assert sol.minSubArrayLen(10, [1, 2, 3, 4]) == 4
assert sol.minSubArrayLen(9, [5, 4, 3, 2, 1]) == 2
assert sol.minSubArrayLen(2, [3]) == 1
assert sol.minSubArrayLen(5, [2, 2, 2]) == 3
assert sol.minSubArrayLen(3, [4]) == 1
assert sol.minSubArrayLen(11, [5, 4, 3, 2, 1]) == 3
assert sol.minSubArrayLen(6, [1, 2, 3, 4]) == 2
assert sol.minSubArrayLen(5, [6, 7]) == 1
assert sol.minSubArrayLen(6, [3, 4]) == 2
assert sol.minSubArrayLen(5, [2, 4]) == 2
assert sol.minSubArrayLen(6, [1, 10]) == 1
