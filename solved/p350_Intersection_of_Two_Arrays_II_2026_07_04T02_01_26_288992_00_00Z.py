"""
URL: https://leetcode.com/problems/intersection-of-two-arrays-ii/description/?envType=problem-list-v2&envId=vn57k9wr

350. Intersection of Two Arrays II

Given two integer arrays nums1 and nums2, return an array of their intersection.
Each element in the result must appear as many times as it shows in both arrays
and you may return the result in any order.


Example 1:

Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2,2]

Example 2:

Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [4,9]
Explanation: [9,4] is also accepted.


Constraints:

    1 <= nums1.length, nums2.length <= 1000
    0 <= nums1[i], nums2[i] <= 1000


Follow up:

    - What if the given array is already sorted? How would you optimize your algorithm?
    - What if nums1's size is small compared to nums2's size? Which algorithm is better?
    - What if elements of nums2 are stored on disk, and the memory is limited such that
      you cannot load all elements into the memory at once?
"""

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        res = []
        c1 = Counter(nums1)
        c2 = Counter(nums2)
        for n in c1 & c2:
            res.extend([n] * min(c1[n], c2[n]))
        return res


sol = Solution()

# print(sol.intersect([1, 2, 2, 1], [2, 2]))  # [2, 2]

assert sorted(sol.intersect([1, 2, 2, 1], [2, 2])) == [2, 2]
assert sorted(sol.intersect([4, 9, 5], [9, 4, 9, 8, 4])) == [4, 9]
assert sol.intersect([1], [1]) == [1]
assert sol.intersect([1], [2]) == []
assert sol.intersect([1, 2, 3], [4, 5, 6]) == []
assert sol.intersect([1, 1, 1], [1, 1]) == [1, 1]
assert sol.intersect([1, 1], [1, 1, 1]) == [1, 1]
assert sol.intersect([2, 2, 2, 2], [2]) == [2]
assert sol.intersect([5], [5, 5, 5, 5]) == [5]
assert sol.intersect([0], [0]) == [0]
assert sol.intersect([1000], [1000]) == [1000]
assert sorted(sol.intersect([0, 0, 1000], [0, 1000, 1000])) == [0, 1000]
assert sorted(sol.intersect([3, 1, 2], [1, 2, 3])) == [1, 2, 3]
assert sol.intersect([2, 1], [1, 2]) == [2, 1]
assert sol.intersect([4, 9, 5], [9, 4, 9, 8, 4]) == [4, 9]
assert len(sol.intersect(list(range(1000)), list(range(1000)))) == 1000
assert sol.intersect([7, 8, 7, 8], [8, 7]) == [7, 8]
assert sorted(sol.intersect([1, 2, 2, 3, 3, 3], [3, 3, 2, 1, 1])) == [1, 2, 3, 3]
assert sol.intersect([0, 1, 0, 1], [0, 0]) == [0, 0]