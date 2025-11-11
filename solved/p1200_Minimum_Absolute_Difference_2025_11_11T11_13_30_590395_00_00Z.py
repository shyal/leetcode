"""
URL: https://leetcode.com/problems/minimum-absolute-difference/description/?envType=problem-list-v2&envId=vn57k9wr

1200. Minimum Absolute Difference

Given an array of distinct integers arr, find all pairs of elements with the minimum absolute difference of any two elements.

Return a list of pairs in ascending order(with respect to pairs), each pair [a, b] follows

- a, b are from arr
- a < b
- b - a equals to the minimum absolute difference of any two elements in arr


Example 1:

Input: arr = [4,2,1,3]
Output: [[1,2],[2,3],[3,4]]
Explanation: The minimum absolute difference is 1. List all pairs with difference equal to 1 in ascending order.

Example 2:

Input: arr = [1,3,6,10,15]
Output: [[1,3]]

Example 3:

Input: arr = [3,8,-10,23,19,-4,-14,27]
Output: [[-14,-10],[19,23],[23,27]]


Constraints:

    2 <= arr.length <= 10^5
    -10^6 <= arr[i] <= 10^6
"""


class Solution:

    def bruteForce(self, arr):
        res = []
        min_abs_diff = maxsize
        for a, b in combinations(arr, 2):
            diff = abs(a - b)
            if diff < min_abs_diff:
                min_abs_diff = diff
                res = []
            if diff == min_abs_diff:
                res.append([*sorted([a, b])])
        return [*sorted(res)]

    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        res = []
        _min = maxsize
        for i in range(1, len(arr)):
            diff = abs(arr[i - 1] - arr[i])
            if diff < _min:
                res = []
                _min = diff
            if diff == _min:
                res.append([arr[i - 1], arr[i]])
        return res


sol = Solution()

print(sol.minimumAbsDifference([4, 2, 1, 3]))  # [[1,2],[2,3],[3,4]]

assert sol.minimumAbsDifference([4, 2, 1, 3]) == [[1, 2], [2, 3], [3, 4]]
assert sol.minimumAbsDifference([1, 3, 6, 10, 15]) == [[1, 3]]
assert sol.minimumAbsDifference([3, 8, -10, 23, 19, -4, -14, 27]) == [
    [-14, -10],
    [19, 23],
    [23, 27],
]
assert sol.minimumAbsDifference([1, 2]) == [[1, 2]]
assert sol.minimumAbsDifference([5, 1]) == [[1, 5]]
assert sol.minimumAbsDifference([-1, 0, 1]) == [[-1, 0], [0, 1]]
assert sol.minimumAbsDifference([10, 20, 25, 27]) == [[25, 27]]
assert sol.minimumAbsDifference([1, 3, 5, 7]) == [[1, 3], [3, 5], [5, 7]]
assert sol.minimumAbsDifference([4, 3, 2, 1, 0, -1, -2]) == [
    [-2, -1],
    [-1, 0],
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
]
assert sol.minimumAbsDifference([1, 100, 101, 200]) == [[100, 101]]
assert sol.minimumAbsDifference([-1000000, 1000000]) == [[-1000000, 1000000]]
assert sol.minimumAbsDifference([0, -1000000, 1000000]) == [[-1000000, 0], [0, 1000000]]
assert sol.minimumAbsDifference([2, 4, 6, 8, 10]) == [[2, 4], [4, 6], [6, 8], [8, 10]]
