"""
URL: https://leetcode.com/problems/minimum-subsequence-in-non-increasing-order/description/?envType=problem-list-v2&envId=vn57k9wr

1403. Minimum Subsequence in Non-Increasing Order

Given the array nums, obtain a subsequence of the array whose sum of elements
is strictly greater than the sum of the non included elements in such
subsequence.

If there are multiple solutions, return the subsequence with minimum size and
if there still exist multiple solutions, return the subsequence with the
maximum total sum of all its elements. A subsequence of an array can be
obtained by erasing some (possibly zero) elements from the array.

Note that the solution with the given constraints is guaranteed to be unique.
Also return the answer sorted in non-increasing order.


Example 1:

Input: nums = [4,3,10,9,8]
Output: [10,9]
Explanation: The subsequences [10,9] and [10,8] are minimal such that the sum
of their elements is strictly greater than the sum of elements not included.
However, the subsequence [10,9] has the maximum total sum of its elements.

Example 2:

Input: nums = [4,4,7,6,7]
Output: [7,7,6]
Explanation: The subsequence [7,7] has the sum of its elements equal to 14
which is not strictly greater than the sum of elements not included
(14 = 4 + 4 + 6). Therefore, the subsequence [7,6,7] is the minimal satisfying
the conditions. Note the subsequence has to be returned in non-increasing
order.


Constraints:

    1 <= nums.length <= 500
    1 <= nums[i] <= 100

---

Solved. Could be optimized (e.g prefix sum). Also shocked this question is tagged 'easy'.
"""

class Solution:

    def findSubsequence(self, nums, k):
        _sum = 0
        total = self.total
        count = len(nums)
        candidates = []
        for i, v in enumerate(nums):
            _sum += v
            total -= v
            count -= 1
            if _sum < total and count == k:
                candidates.append(nums[i+1:])
                return nums[i+1:]
        return None

    def minSubsequence(self, nums: List[int]) -> List[int]:
        if len(nums) == 1:
            return nums
        if len(nums) == 2 and len(set(nums)) == 1:
            return nums
        nums.sort()
        self.total = sum(nums)

        low = 1
        high = len(nums)
        result = None
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            ss = self.findSubsequence(nums, mid)
            if ss:
                result = ss
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if is_minimization:
                    low = mid + 1
                else:
                    high = mid - 1

        return result[::-1] if result else []


sol = Solution()

print(sol.minSubsequence([3, 4, 8, 9, 10]))  # [10, 9]
# print(sol.minSubsequence([4, 3, 10, 9, 8]))  # [10, 9]

assert sol.minSubsequence([4, 3, 10, 9, 8]) == [10, 9]
assert sol.minSubsequence([4, 4, 7, 6, 7]) == [7, 7, 6]
assert sol.minSubsequence([6]) == [6]
assert sol.minSubsequence([1]) == [1]
assert sol.minSubsequence([100]) == [100]
assert sol.minSubsequence([2, 1]) == [2]
assert sol.minSubsequence([1, 2]) == [2]
assert sol.minSubsequence([3, 3]) == [3, 3]
assert sol.minSubsequence([1, 1]) == [1, 1]
assert sol.minSubsequence([5, 5, 5, 5]) == [5, 5, 5]
assert sol.minSubsequence([100, 100, 100, 100]) == [100, 100, 100]
assert sol.minSubsequence([1, 1, 1]) == [1, 1]
assert sol.minSubsequence([100, 1, 1, 1]) == [100]
assert sol.minSubsequence([1, 1, 1, 100]) == [100]
assert sol.minSubsequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [10, 9, 8, 7]
assert sol.minSubsequence([5, 4, 4, 3]) == [5, 4]
assert sol.minSubsequence([3, 2, 2, 1]) == [3, 2]
assert sol.minSubsequence([2, 3, 2]) == [3, 2]
assert sol.minSubsequence([1] * 500) == [1] * 251
assert sol.minSubsequence([100] * 500) == [100] * 251
nums_in = [4, 3, 10, 9, 8]
out = sol.minSubsequence(nums_in)
assert out == [10, 9]
assert all(out[i] >= out[i + 1] for i in range(len(out) - 1))
assert sum(out) > sum(nums_in) - sum(out)