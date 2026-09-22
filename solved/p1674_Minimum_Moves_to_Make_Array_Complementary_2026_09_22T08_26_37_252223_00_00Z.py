"""
URL: https://leetcode.com/problems/minimum-moves-to-make-array-complementary/description/?envType=problem-list-v2&envId=vn57k9wr

1674. Minimum Moves to Make Array Complementary

You are given an integer array nums of even length n and an integer limit. In one move, you can replace any integer from nums with another integer between 1 and limit, inclusive.

The array nums is complementary if for all indices i (0-indexed), nums[i] + nums[n - 1 - i] equals the same number. For example, the array [1,2,3,4] is complementary because for all indices i, nums[i] + nums[n - 1 - i] = 5.

Return the minimum number of moves required to make nums complementary.

Example 1:

Input: nums = [1,2,4,3], limit = 4
Output: 1
Explanation: In 1 move, you can change nums to [1,2,2,3] (underlined elements are changed).
nums[0] + nums[3] = 1 + 3 = 4.
nums[1] + nums[2] = 2 + 2 = 4.
nums[2] + nums[1] = 2 + 2 = 4.
nums[3] + nums[0] = 3 + 1 = 4.
Therefore, nums[i] + nums[n-1-i] = 4 for every i, so nums is complementary.

Example 2:

Input: nums = [1,2,2,1], limit = 2
Output: 2
Explanation: In 2 moves, you can change nums to [2,2,2,2]. You cannot change any number to 3 since 3 > limit.

Example 3:

Input: nums = [1,2,1,2], limit = 2
Output: 0
Explanation: nums is already complementary.

Constraints:

    n == nums.length
    2 <= n <= 10^5
    1 <= nums[i] <= limit <= 10^5
    n is even.

---

Assisted. Most inattention errors, like confusing a, b with lo, hi

LEETCODE: Time Limit Exceeded (63/114 cases)
"""


class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        knobs = lambda a, b: (min(a, b) + 1, max(a, b) + limit)

        def cost(i, T):
            a, b = nums[i], nums[~i]
            lo, hi = knobs(nums[i], nums[~i])
            if a + b == T:
                return 0
            if lo <= T <= hi:
                return 1
            return 2

        def nums_cost(T):
            return sum(cost(i, T) for i in range(len(nums) // 2))

        return min(nums_cost(T) for T in range(2, 2 * limit + 1))


sol = Solution()

print(sol.minMoves([1, 2, 4, 3], 4))  # 1

assert sol.minMoves([1, 2, 4, 3], 4) == 1
assert sol.minMoves([1, 2, 2, 1], 2) == 2
assert sol.minMoves([1, 2, 1, 2], 2) == 0

assert sol.minMoves([1, 1], 1) == 0
assert sol.minMoves([1, 1, 1, 1], 1) == 0
assert sol.minMoves([1, 100000, 1, 100000], 100000) == 0
assert sol.minMoves([100000, 100000, 100000, 100000], 100000) == 0
assert sol.minMoves([1, 2, 3, 4, 5, 6], 6) == 0
assert sol.minMoves([2, 2, 2, 2, 2, 2], 2) == 0
assert sol.minMoves([1, 2, 3, 4, 5, 6, 7, 8], 8) == 0
assert sol.minMoves([1, 1, 1, 1, 1, 1, 1, 1], 1) == 0
assert sol.minMoves([1, 100000, 1, 100000, 1, 100000, 1, 100000], 100000) == 0
assert sol.minMoves([5, 5, 5, 5, 5, 5, 5, 5], 5) == 0
assert sol.minMoves([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 0
assert sol.minMoves([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 10) == 0
