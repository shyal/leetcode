"""
URL: https://leetcode.com/problems/make-array-non-decreasing/description/?envType=problem-list-v2&envId=vn57k9wr

3523. Make Array Non-decreasing

You are given an integer array nums. In one operation, you can select a subarray and replace it with a single element equal to its maximum value.

Return the maximum possible size of the array after performing zero or more operations such that the resulting array is non-decreasing.

Example 1:

Input: nums = [4,2,5,3,5]
Output: 3
Explanation:
One way to achieve the maximum size is:
1) Replace subarray nums[1..2] = [2, 5] with 5 -> [4, 5, 3, 5].
2) Replace subarray nums[2..3] = [3, 5] with 5 -> [4, 5, 5].
The final array [4, 5, 5] is non-decreasing with size 3.

Example 2:

Input: nums = [1,2,3]
Output: 3
Explanation:
No operation is needed as the array [1,2,3] is already non-decreasing.

Constraints:

    1 <= nums.length <= 2 * 10^5
    1 <= nums[i] <= 2 * 10^5

---

LEETCODE: Accepted (72 ms, 40.3 MB)
"""


# mu 0.10
# class Solution
#   def maximumPossibleSize(nums: [int]) -> int
#     _max = nums[0]
#     count = 0
#     for n in nums[1:]
#       if n < _max
#         count += 1
#       if n > _max
#         _max = n
#     len(nums) - count

class Solution:
    def maximumPossibleSize(self, nums: list[int]) -> int:
        _max = nums[0]
        count = 0
        for n in nums[1:]:
            if n < _max:
                count += 1
            if n > _max:
                _max = n
        return len(nums) - count


sol = Solution()
print(sol.maximumPossibleSize([4, 2, 5, 3, 5]))
_l, _r = sol.maximumPossibleSize([4, 2, 5, 3, 5]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([1, 2, 3]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([2, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize(list(range(1, 11))), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize(list(range(10, 0, -1))), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([5] * 10), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([5, 1, 5, 1, 5, 1]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([-3, -2, -1]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([0, -1, -2, -3]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([1, 3, 2, 4, 3, 5]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize([200000, 1, 200000, 1, 200000]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maximumPossibleSize(list(range(1000, 0, -1))), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
