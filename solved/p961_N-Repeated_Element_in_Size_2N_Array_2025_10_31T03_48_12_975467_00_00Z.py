"""
URL: https://leetcode.com/problems/n-repeated-element-in-size-2n-array/description/?envType=problem-list-v2&envId=vn57k9wr

961. N-Repeated Element in Size 2N Array

You are given an integer array nums with the following properties:

- nums.length == 2 * n.
- nums contains n + 1 unique elements.
- Exactly one element of nums is repeated n times.

Return the element that is repeated n times.

Example 1:

Input: nums = [1,2,3,3]
Output: 3

Example 2:

Input: nums = [2,1,2,5,3,2]
Output: 2

Example 3:

Input: nums = [5,1,5,2,5,3,5,4]
Output: 5

Constraints:

- 2 <= n <= 5000
- nums.length == 2 * n
- 0 <= nums[i] <= 10^4
- nums contains n + 1 unique elements and one of them is repeated exactly n times.
"""


class Solution:
    def repeatedNTimes(self, nums: List[int]) -> int:
        return next(
            iter(
                next(
                    iter(
                        sorted(Counter(nums).items(), reverse=True, key=lambda x: x[1])
                    )
                )
            )
        )


sol = Solution()

# print(sol.repeatedNTimes([1, 2, 3, 3]))  # 3

assert sol.repeatedNTimes([1, 2, 3, 3]) == 3
assert sol.repeatedNTimes([2, 1, 2, 5, 3, 2]) == 2
assert sol.repeatedNTimes([5, 1, 5, 2, 5, 3, 5, 4]) == 5
assert sol.repeatedNTimes([3, 3, 1, 2]) == 3
assert sol.repeatedNTimes([0, 0, 1, 2]) == 0
assert sol.repeatedNTimes([10000, 10000, 0, 1]) == 10000
assert sol.repeatedNTimes([1, 2, 3, 1, 4, 1]) == 1
assert sol.repeatedNTimes([2, 3, 4, 1, 1, 1]) == 1
assert sol.repeatedNTimes([1, 2, 1, 3]) == 1
