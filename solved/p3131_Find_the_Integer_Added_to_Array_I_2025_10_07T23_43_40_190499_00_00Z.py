"""
URL: https://leetcode.com/problems/find-the-integer-added-to-array-i/description/

3131. Find the Integer Added to Array I

You are given two arrays of equal length, nums1 and nums2.

Each element in nums1 has been increased (or decreased in the case of negative) by an integer, represented by the variable x.

As a result, nums1 becomes equal to nums2. Two arrays are considered equal when they contain the same integers with the same frequencies.

Return the integer x.


Example 1:

Input: nums1 = [2,6,4], nums2 = [9,7,5]

Output: 3

Explanation:

The integer added to each element of nums1 is 3.

Example 2:

Input: nums1 = [10], nums2 = [5]

Output: -5

Explanation:

The integer added to each element of nums1 is -5.

Example 3:

Input: nums1 = [1,1,1,1], nums2 = [1,1,1,1]

Output: 0

Explanation:

The integer added to each element of nums1 is 0.


Constraints:

        1 <= nums1.length == nums2.length <= 100
        0 <= nums1[i], nums2[i] <= 1000
        The test cases are generated in a way that there is an integer x such that nums1 can become equal to nums2 by adding x to each element of nums1.
"""


class Solution:
    def addedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        x = min(nums2) - min(nums1)
        return x


sol = Solution()
res = sol.addedInteger(nums1=[2, 6, 4], nums2=[9, 7, 5])
# print(res)
assert sol.addedInteger([2, 6, 4], [9, 7, 5]) == 3
assert sol.addedInteger([10], [5]) == -5
assert sol.addedInteger([1, 1, 1, 1], [1, 1, 1, 1]) == 0
assert sol.addedInteger([0], [0]) == 0
assert sol.addedInteger([0], [1000]) == 1000
assert sol.addedInteger([1000], [0]) == -1000
assert sol.addedInteger([0, 500, 1000], [100, 600, 1100]) == 100
assert sol.addedInteger([1, 2, 3, 4, 5], [0, 1, 2, 3, 4]) == -1
assert sol.addedInteger([0, 0, 0], [999, 999, 999]) == 999
assert sol.addedInteger([123], [123]) == 0
assert sol.addedInteger([5, 4, 3, 2, 1], [10, 9, 8, 7, 6]) == 5
