"""
URL: https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/description/?envType=problem-list-v2&envId=vn57k9wr

1760. Minimum Limit of Balls in a Bag

You are given an integer array nums where the i-th bag contains nums[i] balls. You are also given an integer maxOperations.

You can perform the following operation at most maxOperations times:

- Take any bag of balls and divide it into two new bags with a positive number of balls.
  - For example, a bag of 5 balls can become two new bags of 1 and 4 balls, or two new bags of 2 and 3 balls.

Your penalty is the maximum number of balls in a bag. You want to minimize your penalty after the operations.

Return the minimum possible penalty after performing the operations.

Example 1:

Input: nums = [9], maxOperations = 2
Output: 3
Explanation:
- Divide the bag with 9 balls into two bags of sizes 6 and 3. [9] -> [6,3].
- Divide the bag with 6 balls into two bags of sizes 3 and 3. [6,3] -> [3,3,3].
The bag with the most number of balls has 3 balls, so your penalty is 3 and you should return 3.

Example 2:

Input: nums = [2,4,8,2], maxOperations = 4
Output: 2
Explanation:
- Divide the bag with 8 balls into two bags of sizes 4 and 4. [2,4,8,2] -> [2,4,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,4,4,4,2] -> [2,2,2,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,4,4,2] -> [2,2,2,2,2,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,2,2,4,2] -> [2,2,2,2,2,2,2,2].
The bag with the most number of balls has 2 balls, so your penalty is 2, and you should return 2.

Constraints:

- 1 <= nums.length <= 10^5
- 1 <= maxOperations, nums[i] <= 10^9
"""


class Solution:

    def check_condition(self, nums, penalty):
        res = 0
        for n in nums:
            if n > penalty:
                res += ceil_div(n, penalty) - 1
        return res

    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        low = 1
        high = max(nums)
        res = -1
        if maxOperations == 0:
            return high
        while low <= high:
            mid = (low + high) // 2
            ops = self.check_condition(nums, mid)
            if ops <= maxOperations:
                res = mid
                high = mid - 1
            else:
                low = mid + 1
        return res


sol = Solution()

# print(sol.check_condition([9], 3))
# print(sol.check_condition([2, 4, 8, 2], 2))


assert sol.minimumSize([9], 2) == 3
assert sol.minimumSize([2, 4, 8, 2], 4) == 2
assert sol.minimumSize([1], 0) == 1
assert sol.minimumSize([1], 1) == 1
assert sol.minimumSize([2], 0) == 2
assert sol.minimumSize([2], 1) == 1
assert sol.minimumSize([1000000000], 0) == 1000000000
assert sol.minimumSize([1000000000], 1) == 500000000
assert sol.minimumSize([7, 17], 3) == 6
assert sol.minimumSize([4, 4], 1) == 4
assert sol.minimumSize([4, 4], 2) == 2
assert sol.minimumSize([3], 1) == 2
assert sol.minimumSize([3], 2) == 1
assert sol.minimumSize([1, 1, 1], 0) == 1
assert sol.minimumSize([1, 1, 1], 10) == 1
assert sol.minimumSize([5, 5, 5], 4) == 3
assert sol.minimumSize([6], 3) == 2
assert sol.minimumSize([100], 10) == 10
