"""
DRILL: Order By Other Array

Given two integer arrays nums1 and nums2 of equal length, return the values
of nums1 reordered so that the nums2 values at the same indices run from
smallest to largest. All values of nums2 are distinct.

Example 1:

Input: nums1 = [1, 3, 3, 2], nums2 = [2, 1, 3, 4]
Output: [3, 1, 3, 2]
Explanation: nums2 from smallest to largest is 1, 2, 3, 4 at indices 1, 0, 2, 3.

Example 2:

Input: nums1 = [4, 2, 3, 1, 1], nums2 = [7, 5, 10, 9, 6]
Output: [2, 1, 4, 1, 3]

Example 3:

Input: nums1 = [5, 6, 7], nums2 = [3, 2, 1]
Output: [7, 6, 5]

Constraints:

    1 <= len(nums1) == len(nums2) <= 10^5
    0 <= nums1[i], nums2[i] <= 10^5
    All values of nums2 are distinct.

    REQUIRED: O(n log n), one sort call. NO loop that picks the smallest
    remaining nums2 each round.
"""


class Solution:
    def orderByOther(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return [
            x[0] for x in sorted(zip(nums1, nums2), key=lambda x: x[1])
        ]


sol = Solution()

print(sol.orderByOther([1, 3, 3, 2], [2, 1, 3, 4]))  # [3, 1, 3, 2]

assert sol.orderByOther([1, 3, 3, 2], [2, 1, 3, 4]) == [3, 1, 3, 2]
assert sol.orderByOther([4, 2, 3, 1, 1], [7, 5, 10, 9, 6]) == [2, 1, 4, 1, 3]
assert sol.orderByOther([5, 6, 7], [3, 2, 1]) == [7, 6, 5]
assert sol.orderByOther([9, 8], [2, 1]) == [8, 9]
assert sol.orderByOther([4], [0]) == [4]
assert sol.orderByOther(list(range(100000)), list(range(100000))) == list(range(100000))
