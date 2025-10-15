"""
URL: https://leetcode.com/problems/two-out-of-three/description/?envType=problem-list-v2&envId=v0n2n1sc

2032. Two Out of Three

Given three integer arrays nums1, nums2, and nums3, return a distinct array containing all the values that are present in at least two out of the three arrays. You may return the values in any order.

Example 1:

Input: nums1 = [1,1,3,2], nums2 = [2,3], nums3 = [3]
Output: [3,2]
Explanation: The values that are present in at least two arrays are:
- 3, in all three arrays.
- 2, in nums1 and nums2.

Example 2:

Input: nums1 = [3,1], nums2 = [2,3], nums3 = [1,2]
Output: [2,3,1]
Explanation: The values that are present in at least two arrays are:
- 2, in nums2 and nums3.
- 3, in nums1 and nums2.
- 1, in nums1 and nums3.

Example 3:

Input: nums1 = [1,2,2], nums2 = [4,3,3], nums3 = [5]
Output: []
Explanation: No value is present in at least two arrays.


Constraints:

        1 <= nums1.length, nums2.length, nums3.length <= 100
        1 <= nums1[i], nums2[j], nums3[k] <= 100
"""


class Solution:
    def twoOutOfThree(
        self, nums1: List[int], nums2: List[int], nums3: List[int]
    ) -> List[int]:
        a = set(nums1)
        b = set(nums2)
        c = set(nums3)
        res = set([])
        for v in a | b | c:
            if (v in a and v in b) or (v in b and v in c) or (v in a and v in c):
                res.add(v)
        return list(res)


sol = Solution()

assert sol.twoOutOfThree(nums1=[1, 1, 3, 2], nums2=[2, 3], nums3=[3]) == [2, 3]
assert sol.twoOutOfThree(nums1=[3, 1], nums2=[2, 3], nums3=[1, 2]) == [1, 2, 3]
assert sol.twoOutOfThree(nums1=[1, 2, 2], nums2=[4, 3, 3], nums3=[5]) == []
