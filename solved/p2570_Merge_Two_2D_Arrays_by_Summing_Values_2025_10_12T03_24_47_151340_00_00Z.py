"""
URL: https://leetcode.com/problems/merge-two-2d-arrays-by-summing-values/description/

2570. Merge Two 2D Arrays by Summing Values

You are given two 2D integer arrays nums1 and nums2.

    nums1[i] = [idi, vali] where all the idi are distinct.
    Similarly for nums2.

Return the 2D array where for each id that appears in nums1 or nums2, the value is the sum of all vali for that id (if id appears in both, sum their values). The returned array must be sorted in ascending order by id.


Example 1:

Input: nums1 = [[1,2],[2,3],[4,5]], nums2 = [[1,4],[3,2],[4,1]]
Output: [[1,6],[2,3],[3,2],[4,6]]
Explanation: The ids are:
- 1: val=2 in nums1, val=4 in nums2 → sum=6
- 2: val=3 in nums1 → sum=3
- 3: val=2 in nums2 → sum=2
- 4: val=5 in nums1, val=1 in nums2 → sum=6
Sorted by id: [[1,6],[2,3],[3,2],[4,6]]

Example 2:

Input: nums1 = [[2,4],[3,6],[5,5]], nums2 = [[1,3],[4,3]]
Output: [[1,3],[2,4],[3,6],[4,3],[5,5]]


Constraints:

    1 <= nums1.length, nums2.length <= 200
    nums1[i].length == nums2[j].length == 2
    1 <= idi, vali <= 1000
    All idi in nums1 are distinct.
    All idi in nums2 are distinct.
"""


class Solution:
    def mergeArrays(
        self, nums1: List[List[int]], nums2: List[List[int]]
    ) -> List[List[int]]:
        dd = defaultdict(int)
        for i, n in chain(nums1, nums2):
            dd[i] += n
        return [*sorted([list(x) for x in dd.items()], key=lambda x: x[0])]


sol = Solution()

# print(sol.mergeArrays([[1, 2], [2, 3], [4, 5]], [[1, 4], [3, 2], [4, 1]]))

assert sol.mergeArrays([[1, 2], [2, 3], [4, 5]], [[1, 4], [3, 2], [4, 1]]) == [
    [1, 6],
    [2, 3],
    [3, 2],
    [4, 6],
]
assert sol.mergeArrays([[2, 4], [3, 6], [5, 5]], [[1, 3], [4, 3]]) == [
    [1, 3],
    [2, 4],
    [3, 6],
    [4, 3],
    [5, 5],
]
assert sol.mergeArrays([[1, 2]], [[3, 4]]) == [[1, 2], [3, 4]]
assert sol.mergeArrays([[1, 2]], [[1, 3]]) == [[1, 5]]
assert sol.mergeArrays([[1, 1], [3, 3], [5, 5]], [[2, 2]]) == [
    [1, 1],
    [2, 2],
    [3, 3],
    [5, 5],
]
assert sol.mergeArrays([[1, 1], [2, 2]], [[1, 10], [2, 20]]) == [[1, 11], [2, 22]]
assert sol.mergeArrays([[1000, 1000]], [[1, 1]]) == [[1, 1], [1000, 1000]]
assert sol.mergeArrays([[4, 1], [2, 1], [1, 1]], [[3, 1], [5, 1]]) == [
    [1, 1],
    [2, 1],
    [3, 1],
    [4, 1],
    [5, 1],
]
assert sol.mergeArrays([[1, 1]], [[1, 1]]) == [[1, 2]]
assert sol.mergeArrays([[500, 500], [600, 600]], [[500, 500]]) == [
    [500, 1000],
    [600, 600],
]
assert sol.mergeArrays([], []) == []
assert sol.mergeArrays([], [[1, 1]]) == [[1, 1]]
