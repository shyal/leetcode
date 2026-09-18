"""
DRILL: Indices By Value
SNIPPET: lcargsort

Given an integer array nums2 of length n, return the indices 0 to n - 1
ordered so that their nums2 values run from smallest to largest. When two
indices have the same nums2 value, the smaller index comes first.

Example 1:

Input: nums2 = [2, 1, 3, 4]
Output: [1, 0, 2, 3]
Explanation: nums2[1] = 1, nums2[0] = 2, nums2[2] = 3, nums2[3] = 4.

Example 2:

Input: nums2 = [7, 5, 10, 9, 6]
Output: [1, 4, 0, 3, 2]

Example 3:

Input: nums2 = [3, 1, 3]
Output: [1, 0, 2]
Explanation: Indices 0 and 2 both hold 3, so 0 comes first.

Constraints:

    1 <= n <= 10^5
    0 <= nums2[i] <= 10^5

    REQUIRED: O(n log n), one sort call. NO sorting the values and then
    searching for the index of each one.
"""


class Solution:
    def indicesByValue(self, nums2: List[int]) -> List[int]:
        return [x[1] for x in sorted(zip(nums2, range(len(nums2))), key=lambda x: x[0])]


sol = Solution()

print(sol.indicesByValue([2, 1, 3, 4]))  # [1, 0, 2, 3]

assert sol.indicesByValue([2, 1, 3, 4]) == [1, 0, 2, 3]
assert sol.indicesByValue([7, 5, 10, 9, 6]) == [1, 4, 0, 3, 2]
assert sol.indicesByValue([3, 1, 3]) == [1, 0, 2]
assert sol.indicesByValue([5, 5, 5]) == [0, 1, 2]
assert sol.indicesByValue([0]) == [0]
assert sol.indicesByValue(list(range(100000))) == list(range(100000))
