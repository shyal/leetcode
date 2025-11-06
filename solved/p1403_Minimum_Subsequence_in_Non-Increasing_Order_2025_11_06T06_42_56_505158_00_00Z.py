"""
URL: https://leetcode.com/problems/minimum-subsequence-in-non-increasing-order/description/?envType=problem-list-v2&envId=vn57k9wr

1403. Minimum Subsequence in Non-Increasing Order

Given the array nums, obtain a subsequence of the array whose sum of elements is strictly greater than the sum of the non included elements in such subsequence.

If there are multiple solutions, return the subsequence with minimum size and if there still exist multiple solutions, return the subsequence with the maximum total sum of all its elements. A subsequence of an array can be obtained by erasing some (possibly zero) elements from the array.

Note that the solution with the given constraints is guaranteed to be unique. Also return the answer sorted in non-increasing order.


Example 1:

Input: nums = [4,3,10,9,8]
Output: [10,9]
Explanation: The subsequences [10,9] and [10,8] are minimal such that the sum of their elements is strictly greater than the sum of elements not included. However, the subsequence [10,9] has the maximum total sum of its elements.

Example 2:

Input: nums = [4,4,7,6,7]
Output: [7,7,6]
Explanation: The subsequence [7,7] has the sum of its elements equal to 14 which is not strictly greater than the sum of elements not included (14 = 4 + 4 + 6). Therefore, the subsequence [7,6,7] is the minimal satisfying the conditions. Note the subsequence has to be returned in non-increasing order.


Constraints:

    1 <= nums.length <= 500
    1 <= nums[i] <= 100
"""


class Solution:
    def minSubsequence(self, nums: List[int]) -> List[int]:
        nums.sort()
        s = 0
        _sum = sum(nums)
        ss = []
        while nums and s <= _sum:
            e = nums.pop()
            s += e
            _sum -= e
            ss.append(e)
        return ss


sol = Solution()

# print(sol.minSubsequence([4, 3, 10, 9, 8]))  # [10,9]

assert sol.minSubsequence([4, 3, 10, 9, 8]) == [10, 9]
assert sol.minSubsequence([4, 4, 7, 6, 7]) == [7, 7, 6]
assert sol.minSubsequence([1]) == [1]
assert sol.minSubsequence([1, 1]) == [1, 1]
assert sol.minSubsequence([1, 2]) == [2]
assert sol.minSubsequence([2, 2, 2, 2]) == [2, 2, 2]
assert sol.minSubsequence([6, 1, 1, 1]) == [6]
assert sol.minSubsequence([3, 3, 3]) == [3, 3]
assert sol.minSubsequence([100, 100]) == [100, 100]
assert sol.minSubsequence([1, 2, 3]) == [3, 2]
assert sol.minSubsequence([5, 4, 3, 2, 1]) == [5, 4]
assert sol.minSubsequence([100]) == [100]
assert sol.minSubsequence([1, 1, 1, 1, 1]) == [1, 1, 1]
assert sol.minSubsequence([99, 1, 1, 1, 1]) == [99]
assert sol.minSubsequence([50, 50, 50]) == [50, 50]
