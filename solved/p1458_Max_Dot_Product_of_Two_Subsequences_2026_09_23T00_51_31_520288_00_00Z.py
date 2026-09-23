# combo chain: two-sequence-align, problem 11 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/max-dot-product-of-two-subsequences/description/?envType=problem-list-v2&envId=vn57k9wr

1458. Max Dot Product of Two Subsequences

Given two arrays nums1 and nums2.

Return the maximum dot product between non-empty subsequences of nums1 and nums2 with the same length.

A subsequence of an array is a new array which is formed from the original array by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (ie, [2,3,5] is a subsequence of [1,2,3,4,5] while [1,5,3] is not).

Example 1:

Input: nums1 = [2,1,-2,5], nums2 = [3,0,-6]
Output: 18
Explanation: Take subsequence [2,-2] from nums1 and subsequence [3,-6] from nums2.
Their dot product is (2*3 + (-2)*(-6)) = 18.

Example 2:

Input: nums1 = [3,-2], nums2 = [2,-6,7]
Output: 21
Explanation: Take subsequence [3] from nums1 and subsequence [7] from nums2.
Their dot product is (3*7) = 21.

Example 3:

Input: nums1 = [-1,-1], nums2 = [1,1]
Output: -1
Explanation: Take subsequence [-1] from nums1 and subsequence [1] from nums2.
Their dot product is -1.

Constraints:

    1 <= nums1.length, nums2.length <= 500
    -1000 <= nums1[i], nums2[i] <= 1000

---

LEETCODE: Wrong Answer (65/70 cases)
"""


class Solution:
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        nums1, nums2 = [1] + nums1, [1] + nums2
        dp = table(len(nums1), len(nums2), fill=0)
        _max = -inf
        for i, j in cells(dp, start=1):
            dp[i][j] = max(
                nums1[i] * nums2[j] + dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]
            )
            _max = max(dp[i][j], _max)
        # tabulate(dp, headers=list(nums2), row_labels=list(nums1))
        return _max


sol = Solution()

print(sol.maxDotProduct([-1, -1], [1, 1]))  # -1


# assert sol.maxDotProduct([-1, -1], [1, 1]) == -1
# assert sol.maxDotProduct([1] * 500, [-1] * 500) == -1
# assert sol.maxDotProduct([1, 2, 3], [-3, -2, -1]) == -1


assert sol.maxDotProduct([2, 1, -2, 5], [3, 0, -6]) == 18
assert sol.maxDotProduct([3, -2], [2, -6, 7]) == 21
assert sol.maxDotProduct([0], [0]) == 0
assert sol.maxDotProduct([1], [1]) == 1
assert sol.maxDotProduct([-1], [-1]) == 1
assert sol.maxDotProduct([1000] * 500, [1000] * 500) == 500000000
assert sol.maxDotProduct([-1000] * 500, [-1000] * 500) == 500000000
assert sol.maxDotProduct([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == 46
assert sol.maxDotProduct([1, -1, 1, -1], [-1, 1, -1, 1]) == 3
assert sol.maxDotProduct([0] * 500, [1000] * 500) == 0
assert sol.maxDotProduct([1000, -1000] * 250, [-1000, 1000] * 250) == 499000000
assert sol.maxDotProduct([1, 2, 3, 4, 5], [0, 0, 0, 0, 0]) == 0
