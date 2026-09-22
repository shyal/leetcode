# combo chain: two-sequence-align, problem 7 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/maximum-length-of-repeated-subarray/description/?envType=problem-list-v2&envId=vn57k9wr

718. Maximum Length of Repeated Subarray

Given two integer arrays nums1 and nums2, return the maximum length of a subarray that appears in both arrays.

Example 1:

Input: nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
Output: 3
Explanation: The repeated subarray with maximum length is [3,2,1].

Example 2:

Input: nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]
Output: 5
Explanation: The repeated subarray with maximum length is [0,0,0,0,0].

Constraints:

    1 <= nums1.length, nums2.length <= 1000
    0 <= nums1[i], nums2[i] <= 100

---

LEETCODE: Accepted (1531 ms, 44.4 MB)
"""


class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        a, b = ["_"] + nums1, ["."] + nums2
        dp = table(len(a), len(b))
        # tabulate(dp, headers=list(b), row_labels=list(a))
        _max = 0
        for i, j in cells(dp, start=1):
            if a[i] == b[j]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            _max = max(_max, dp[i][j])
        # tabulate(dp, headers=list(b), row_labels=list(a))
        return _max


sol = Solution()

print(sol.findLength([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]))  # 3

assert sol.findLength([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]) == 3
assert sol.findLength([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]) == 5

assert sol.findLength([], []) == 0
assert sol.findLength([1], [1]) == 1
assert sol.findLength([1], [2]) == 0
assert sol.findLength([1, 2, 3], [4, 5, 6]) == 0
assert sol.findLength([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == 1
assert sol.findLength([1, 2, 2, 3, 4], [2, 2, 3, 5]) == 3
assert sol.findLength([-1, -2, -3], [-1, -2, -3]) == 3
# assert sol.findLength([100] * 1000, [100] * 1000) == 1000
# assert sol.findLength([1] * 500 + [2] * 500, [2] * 500 + [1] * 500) == 500
# assert sol.findLength([0] * 999 + [1], [1] + [0] * 999) == 999
# assert sol.findLength([1, 2, 3, 4, 5] * 200, [3, 4, 5, 6, 7] * 200) == 3
# assert sol.findLength([1] * 1000, [2] * 1000) == 0
