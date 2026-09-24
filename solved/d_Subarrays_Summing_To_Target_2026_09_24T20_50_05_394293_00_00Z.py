"""
DRILL: Subarrays Summing To Target

Given an integer array vals and an integer target, return the number of
contiguous subarrays of vals whose elements sum to target. Values can be
negative.

Example 1:

Input: vals = [3, -1, 4, 1, 5, -2, 3], target = 6
Output: 3
Explanation: [3, -1, 4], [1, 5] and [5, -2, 3] sum to 6.

Example 2:

Input: vals = [2, -2, 2, -2], target = 0
Output: 4
Explanation: [2, -2] starting at index 0, [2, -2] starting at index 2,
[-2, 2] and the whole array.

Example 3:

Input: vals = [2, 4, 6, 1, 3], target = 9
Output: 0

Constraints:

    1 <= len(vals) <= 10^5
    -10^4 <= vals[i] <= 10^4
    -10^9 <= target <= 10^9

    REQUIRED: O(n), one pass over vals. NO enumeration of start and end
    pairs. Negative values make a two-pointer scan wrong.
"""


# mu source (current.mu), the candidate's solution. The Python
# under it is the transpiler's output, and it is what ran.
#
# def countSubarrays(vals: [int], target: int) -> int
#   D = defaultdict(int)
#   D[0] = 1
#   prefix = 0
#   res = 0
#   for v in vals
#     prefix += v
#     res += D[prefix - target]
#     D[prefix] += 1
#   res

class Solution:
    def countSubarrays(self, vals: list[int], target: int) -> int:
        D = defaultdict(int)
        D[0] = 1
        prefix = 0
        res = 0
        for v in vals:
            prefix += v
            res += D[prefix - target]
            D[prefix] += 1
        return res


sol = Solution()
print(sol.countSubarrays([3, -1, 4, 1, 5, -2, 3], 6))
assert sol.countSubarrays([3, -1, 4, 1, 5, -2, 3], 6) == 3
assert sol.countSubarrays([2, -2, 2, -2], 0) == 4
assert sol.countSubarrays([2, 4, 6, 1, 3], 9) == 0
assert sol.countSubarrays([5], 5) == 1
assert sol.countSubarrays([5], 4) == 0
assert sol.countSubarrays([1, 1, 1], 2) == 2
assert sol.countSubarrays([1, 2, 3, 4, 5], 5) == 2
assert sol.countSubarrays([4, -1, 2, -1, 4], 3) == 2
assert sol.countSubarrays([1, -1, 1, -1], 0) == 4
assert sol.countSubarrays([0, 0, 0], 0) == 6
assert sol.countSubarrays([1] * 10 ** 5, 10 ** 5) == 1
assert sol.countSubarrays([1] * 10 ** 5, 1) == 10 ** 5
