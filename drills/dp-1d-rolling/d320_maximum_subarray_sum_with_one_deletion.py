"""
Given an integer array nums, return the largest sum of a non-empty
subarray from which at most one element is deleted. The subarray must
stay non-empty after the deletion.

Iterate over nums from the left with two values: the largest sum of a
subarray that ends at the current element with nothing deleted, the kept
value, and the largest sum of a subarray that ends at the current
element with exactly one element deleted, the deleted value. At each
element x, the deleted value is the larger of x plus the previous
deleted value and the previous kept value: in the second case x itself
is the deleted element and the subarray ends at the element before it.
Then the kept value is the larger of x on its own and x plus the
previous kept value. Compute the deleted value first, from the kept
value before it changes. The answer is the largest value seen in either.

For example with nums = [1, -2, 0, 3], the kept values are 1, -1, 0, 3
and the deleted values are none, 1, 1, 4. The answer is 4: delete -2,
the subarray [1, 0, 3].

Example 1:

Input: nums = [1, -2, 0, 3]
Output: 4

Example 2:

Input: nums = [1, -2, -2, 3]
Output: 3
Explanation: the subarray [3]; deleting one -2 leaves 1 - 2 + 3 = 2.

Example 3:

Input: nums = [-1, -1, -1, -1]
Output: -1
Explanation: the subarray cannot be empty, so a deletion leaves at
least one -1.

Constraints:

    1 <= len(nums) <= 10^5
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n) time, O(1) extra space, a single pass. The deleted
    value must read the kept value of the element before x, not the
    kept value that includes x. NO prefix and suffix arrays. The empty
    subarray is not allowed: on [-1, -1, -1, -1] the answer is -1,
    not 0.
"""


class Solution:
    def maximumSum(self, nums: list[int]) -> int:
        pass


sol = Solution()

print(sol.maximumSum([1, -2, 0, 3]))  # 4

# assert sol.maximumSum([1, -2, 0, 3]) == 4
# assert sol.maximumSum([1, -2, -2, 3]) == 3
# assert sol.maximumSum([-1, -1, -1, -1]) == -1
# assert sol.maximumSum([5]) == 5
# assert sol.maximumSum([-5]) == -5
# assert sol.maximumSum([2, -9, 2]) == 4
# assert sol.maximumSum([-9, 2, 2]) == 4
# assert sol.maximumSum([2, 2, -9]) == 4
# assert sol.maximumSum([3, -1, -1, 3]) == 5
# assert sol.maximumSum([8, -1, 6, -7, -8, 5, 4]) == 15
# assert sol.maximumSum([1, 1, 1, -100, 1, 1, 1]) == 6
# assert sol.maximumSum([10 ** 4] * 10 ** 5) == 10 ** 9
# assert sol.maximumSum([-10 ** 4] * 10 ** 5) == -10 ** 4
# assert sol.maximumSum([1, -1] * 50000) == 2
