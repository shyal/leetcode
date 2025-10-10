"""
URL: https://leetcode.com/problems/intersection-of-two-arrays/description/

349. Intersection of Two Arrays

Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.

Example 1:

Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]

Example 2:

Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [4,9]

Constraints:

    1 <= nums1.length, nums2.length <= 1000
    0 <= nums1[i], nums2[i] <= 1000
"""


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1).intersection(nums2))


sol = Solution()

# print(sol.intersection([1, 2, 2, 1], [2, 2]))
assert set(sol.intersection([1, 2, 2, 1], [2, 2])) == {2}
assert set(sol.intersection([4, 9, 5], [9, 4, 9, 8, 4])) == {4, 9}
assert set(sol.intersection([1], [1])) == {1}
assert set(sol.intersection([1, 2, 3], [4, 5, 6])) == set()
assert set(sol.intersection([0, 0, 0], [0])) == {0}
assert set(sol.intersection([1000, 999], [999, 1000])) == {999, 1000}
assert set(sol.intersection([1, 2, 2, 3, 3, 3], [2, 3, 4])) == {2, 3}
assert set(sol.intersection([5], [1, 2, 3, 4, 5])) == {5}
assert set(sol.intersection([1, 1, 1, 1], [1, 1])) == {1}
assert set(sol.intersection([0, 1000], [500])) == set()
assert set(sol.intersection([1, 2], [2, 1])) == {1, 2}
