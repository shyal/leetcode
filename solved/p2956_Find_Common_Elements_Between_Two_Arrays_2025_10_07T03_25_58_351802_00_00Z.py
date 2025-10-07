"""
URL: https://leetcode.com/problems/find-common-elements-between-two-arrays/description/

2956. Find Common Elements Between Two Arrays

Let me reword the description so much easier:

Count how many indices in the first array have a number that exists in the second array. Call this result left
Count how many indices in the second array have a number that exists in the first array. Call this result right

return [left, right]

Example 1:

Input: nums1 = [4,3,2,3,1], nums2 = [2,2,5,2,3,6]
Output: [3,4]
Explanation:
We calculate the values as follows:
- The elements at nums1[1], nums1[2], and nums1[3] are common in nums2.
- The elements at nums2[0], nums2[1], nums2[3], and nums2[4] are common in nums1.

Example 2:

Input: nums1 = [3,1,2,1,1], nums2 = [2,3,2]
Output: [2,3]
Explanation:
We calculate the values as follows:
- The elements at nums1[0] and nums1[2] are common in nums2.
- The elements at nums2[0], nums2[1], and nums2[2] are common in nums1.


Constraints:

    1 <= nums1.length, nums2.length <= 100
    1 <= nums1[i], nums2[i] <= 100

"""


class Solution:
    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        left = 0
        for i in range(len(nums1)):
            if nums1[i] in nums2:
                left += 1
        right = 0
        for i in range(len(nums2)):
            if nums2[i] in nums1:
                right += 1

        return [left, right]


sol = Solution()

assert sol.findIntersectionValues([4, 3, 2, 3, 1], [2, 2, 5, 2, 3, 6]) == [3, 4]
assert sol.findIntersectionValues([3, 1, 2, 1, 1], [2, 3, 2]) == [2, 3]
assert sol.findIntersectionValues([1, 1, 1], [1]) == [3, 1]
assert sol.findIntersectionValues([1, 2, 3], [4, 5, 6]) == [0, 0]
assert sol.findIntersectionValues([1], [1]) == [1, 1]
assert sol.findIntersectionValues([1], [2]) == [0, 0]
assert sol.findIntersectionValues([2, 2, 2], [2, 3, 2]) == [3, 2]
assert sol.findIntersectionValues([100, 100], [100]) == [2, 1]
assert sol.findIntersectionValues([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == [5, 5]
assert sol.findIntersectionValues([5] * 5, [5] * 3) == [5, 3]
assert sol.findIntersectionValues([1, 3, 5, 7, 9], [2, 4, 6, 8, 10]) == [0, 0]
assert sol.findIntersectionValues([1, 1, 2, 2, 3], [3, 3, 4]) == [1, 2]
