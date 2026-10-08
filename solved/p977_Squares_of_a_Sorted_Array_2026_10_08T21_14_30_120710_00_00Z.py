"""
URL: https://leetcode.com/problems/squares-of-a-sorted-array/description/?envType=problem-list-v2&envId=vn57k9wr

977. Squares of a Sorted Array

Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.

Example 1:

Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].

Example 2:

Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]

Constraints:

    1 <= nums.length <= 10^4
    -10^4 <= nums[i] <= 10^4
    nums is sorted in non-decreasing order.

Follow up: Squaring each element and sorting the new array is very trivial, could you find an O(n) solution using a different approach?

---

LEETCODE: Accepted (3 ms, 21.3 MB)
"""


# mu 0.7
# def sortedSquares(nums: [int]) -> [int]
#   list(sorted([x * x for x in nums]))

class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        return list(sorted([x * x for x in nums]))


sol = Solution()
print(sol.sortedSquares([-4, -1, 0, 3, 10]))
_l, _r = sol.sortedSquares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-7, -3, 2, 3, 11]), [4, 9, 9, 49, 121]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([0]), [0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-1]), [1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([1]), [1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-10000, 0, 10000]), [0, 100000000, 100000000]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-2, -2, 0, 2, 2]), [0, 4, 4, 4, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-3, -3, -3]), [9, 9, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([3, 3, 3]), [9, 9, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-10, -5, -5, 0, 5, 5, 10]), [0, 25, 25, 25, 25, 100, 100]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-1, 0, 0, 0, 1]), [0, 0, 0, 1, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sortedSquares([-10000]), [100000000]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
