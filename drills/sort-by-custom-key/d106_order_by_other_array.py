"""
DRILL: Order By Other Array

Given two integer arrays nums1 and nums2 of equal length, return the values
of nums1 reordered so that the nums2 values at the same indices run from
largest to smallest. All values of nums2 are distinct.

Example 1:

Input: nums1 = [1, 3, 3, 2], nums2 = [2, 1, 3, 4]
Output: [2, 3, 1, 3]
Explanation: nums2 from largest to smallest is 4, 3, 2, 1 at indices 3, 2, 0, 1.

Example 2:

Input: nums1 = [4, 2, 3, 1, 1], nums2 = [7, 5, 10, 9, 6]
Output: [3, 1, 4, 1, 2]

Example 3:

Input: nums1 = [5, 6, 7], nums2 = [1, 2, 3]
Output: [7, 6, 5]

Constraints:

    1 <= len(nums1) == len(nums2) <= 10^5
    0 <= nums1[i], nums2[i] <= 10^5
    All values of nums2 are distinct.

    REQUIRED: O(n log n), one sort call. NO loop that picks the largest
    remaining nums2 each round.
"""


class Solution:
    def orderByOther(self, nums1: List[int], nums2: List[int]) -> List[int]:
        pass


sol = Solution()

print(sol.orderByOther([1, 3, 3, 2], [2, 1, 3, 4]))  # [2, 3, 1, 3]

# assert sol.orderByOther([1, 3, 3, 2], [2, 1, 3, 4]) == [2, 3, 1, 3]
# assert sol.orderByOther([4, 2, 3, 1, 1], [7, 5, 10, 9, 6]) == [3, 1, 4, 1, 2]
# assert sol.orderByOther([5, 6, 7], [1, 2, 3]) == [7, 6, 5]
# assert sol.orderByOther([9, 8], [2, 1]) == [9, 8]
# assert sol.orderByOther([4], [0]) == [4]
# assert sol.orderByOther(list(range(100000)), list(range(100000))) == list(range(99999, -1, -1))
