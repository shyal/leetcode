# combo chain: two-sequence-align, problem 2 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/uncrossed-lines/description/?envType=problem-list-v2&envId=vn57k9wr

1035. Uncrossed Lines

You are given two integer arrays nums1 and nums2. We write the integers of nums1 and nums2 (in the order they are given) on two separate horizontal lines.

We may draw connecting lines: a straight line connecting two numbers nums1[i] and nums2[j] such that:

- nums1[i] == nums2[j], and
- the line we draw does not intersect any other connecting (non-horizontal) line.

Note that a connecting line cannot intersect even at the endpoints (i.e., each number can only belong to one connecting line).

Return the maximum number of connecting lines we can draw in this way.

Example 1:

Input: nums1 = [1,4,2], nums2 = [1,2,4]
Output: 2
Explanation: We can draw 2 uncrossed lines as in the diagram.
We cannot draw 3 uncrossed lines, because the line from nums1[1] = 4 to nums2[2] = 4 will intersect the line from nums1[2]=2 to nums2[1]=2.

Example 2:

Input: nums1 = [2,5,1,2,5], nums2 = [10,5,2,1,5,2]
Output: 3

Example 3:

Input: nums1 = [1,3,7,1,7,5], nums2 = [1,9,2,5,1]
Output: 2

Constraints:

    1 <= nums1.length, nums2.length <= 500
    1 <= nums1[i], nums2[j] <= 2000

---

this is part of a combo chain. In my last solve of this question, i correctly
identified this was an LCS question. In this attempt, i did not.

Hinted by reading my chain of thought of previous attempt.

LEETCODE: Accepted (63 ms, 19.7 MB)
"""


class Solution:
    def maxUncrossedLines(self, a: List[int], b: List[int]) -> int:
        a.insert(0, ".")
        b.insert(0, "_")
        dp = table(len(a), len(b))
        for i, j in cells(dp):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[-1][-1]


sol = Solution()

# print(sol.maxUncrossedLines([1, 4, 2], [1, 2, 4]))  # 2
# print(sol.maxUncrossedLines([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1]))  # 2


assert sol.maxUncrossedLines([1, 4, 2], [1, 2, 4]) == 2
assert sol.maxUncrossedLines([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]) == 3
assert sol.maxUncrossedLines([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1]) == 2

assert sol.maxUncrossedLines([], []) == 0
assert sol.maxUncrossedLines([1], [1]) == 1
assert sol.maxUncrossedLines([1], [2]) == 0
assert sol.maxUncrossedLines([1, 1, 1, 1], [1, 1, 1]) == 3
assert sol.maxUncrossedLines([-1, -2, -3], [-3, -2, -1]) == 1
assert sol.maxUncrossedLines([2000] * 500, [2000] * 500) == 500
assert (
    sol.maxUncrossedLines([i for i in range(1, 501)], [i for i in range(500, 0, -1)])
    == 1
)
assert sol.maxUncrossedLines([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == 1
assert sol.maxUncrossedLines([1] * 250 + [2] * 250, [2] * 250 + [1] * 250) == 250
assert sol.maxUncrossedLines([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == 0
assert sol.maxUncrossedLines([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 5
assert sol.maxUncrossedLines([1] * 500, [1] * 500) == 500
