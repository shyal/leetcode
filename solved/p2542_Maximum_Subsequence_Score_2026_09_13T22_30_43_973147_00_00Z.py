"""
URL: https://leetcode.com/problems/maximum-subsequence-score/description/?envType=problem-list-v2&envId=vn57k9wr

2542. Maximum Subsequence Score

You are given two 0-indexed integer arrays nums1 and nums2 of equal length n and a positive integer k. You must choose a subsequence of indices from nums1 of length k.

For chosen indices i0, i1, ..., i(k - 1), your score is defined as:

- The sum of the selected elements from nums1 multiplied with the minimum of the selected elements from nums2.
- It can be defined simply as: (nums1[i0] + nums1[i1] + ... + nums1[i(k - 1)]) * min(nums2[i0], nums2[i1], ..., nums2[i(k - 1)]).

Return the maximum possible score.

A subsequence of indices of an array is a set that can be derived from the set {0, 1, ..., n-1} by deleting some or no elements.

Example 1:

Input: nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
Output: 12
Explanation:
The four possible subsequence scores are:
- We choose the indices 0, 1, and 2 with score = (1+3+3) * min(2,1,3) = 7.
- We choose the indices 0, 1, and 3 with score = (1+3+2) * min(2,1,4) = 6.
- We choose the indices 0, 2, and 3 with score = (1+3+2) * min(2,3,4) = 12.
- We choose the indices 1, 2, and 3 with score = (3+3+2) * min(1,3,4) = 8.
Therefore, we return the max score, which is 12.

Example 2:

Input: nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1
Output: 30
Explanation:
Choosing index 2 is optimal: nums1[2] * nums2[2] = 3 * 10 = 30 is the maximum possible score.

Constraints:

    n == nums1.length == nums2.length
    1 <= n <= 10^5
    0 <= nums1[i], nums2[j] <= 10^5
    1 <= k <= n

---

sum of nums1 selected for k * min of nums1 selected for k

so we need the largest sum of numbers in nums1 and the min in nums1.

But it has to be the same range.



class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        prefix = [*accumulate(nums1)]

        def running_sum(i, j):
            return prefix[j] - (prefix[i - 1] if i > 0 else 0)

        left = 0
        best = 0

        for right in range(k - 1, len(nums2)):
            _min = min(nums2[left : right + 1])
            _sum = running_sum(left, right)
            print(_min * _sum)
            best = max(best, _min * _sum)

        return best

ugh answered the wrong question.. so running low on time now. Let's at least
compute the brute force version:

class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        best = 0
        for comb in combinations(range(len(nums1)), k):
            _nums1 = [nums1[x] for x in comb]
            _nums2 = [nums2[x] for x in comb]
            _sum = sum(_nums1)
            _min = min(_nums2)
            res = _sum * _min
            best = max(best, res)
        return best

The fast version MIGHT be to compute the combinations

hmmm the combs version has max recursion issues too.. so clearly
this is a DP problem i'm not seeing.

"""


class Solution:
    def maxScorebf(self, nums1: List[int], nums2: List[int], k: int) -> int:
        best = 0
        for comb in combinations(range(len(nums1)), k):
            _nums1 = [nums1[x] for x in comb]
            _nums2 = [nums2[x] for x in comb]
            _sum = sum(_nums1)
            _min = min(_nums2)
            res = _sum * _min
            best = max(best, res)
        return best

    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        def helper(i, _sum, _min):
            if len(curr) == k:
                self.res = max(_sum * _min, self.res)
                return
            for j in range(i, len(nums1)):
                curr.append(nums1[j])
                helper(j + 1, _sum + nums1[j], min(_min, nums2[j]))
                curr.pop()

        self.res = 0
        curr = []
        helper(0, 0, float("inf"))
        return self.res


sol = Solution()

print(sol.maxScore([1, 3, 3, 2], [2, 1, 3, 4], 3))  # 12

assert sol.maxScore([1, 3, 3, 2], [2, 1, 3, 4], 3) == 12
assert sol.maxScore([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1) == 30

assert sol.maxScore([0], [0], 1) == 0
# assert sol.maxScore([10**5] * 10**5, [10**5] * 10**5, 10**5) == 1000000000000000
assert sol.maxScore([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 5) == 15
assert sol.maxScore([5, 5, 5, 5], [1, 1, 1, 1], 2) == 10
assert sol.maxScore([1, 2, 3, 4, 5], [5, 5, 5, 5, 5], 3) == 60
assert sol.maxScore([1, 1, 1, 1, 1], [10, 9, 8, 7, 6], 3) == 24
assert sol.maxScore([0, 0, 0, 0], [10, 10, 10, 10], 2) == 0
assert sol.maxScore([1, 2, 3, 4, 5], [0, 0, 0, 0, 0], 3) == 0
assert sol.maxScore([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 1) == 9
assert sol.maxScore([10, 20, 30, 40, 50], [1, 2, 3, 4, 5], 4) == 280
assert sol.maxScore([100, 200, 300], [3, 2, 1], 2) == 600
# assert sol.maxScore([1] * 100000, [100000] * 100000, 50000) == 5000000000
