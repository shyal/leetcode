"""
URL: https://leetcode.com/problems/single-number/description/?envType=problem-list-v2&envId=vn57k9wr

136. Single Number

Given a non-empty array of integers nums, every element appears twice except
for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only
constant extra space.


Example 1:

Input: nums = [2,2,1]
Output: 1

Example 2:

Input: nums = [4,1,2,1,2]
Output: 4

Example 3:

Input: nums = [1]
Output: 1


Constraints:

    1 <= nums.length <= 3 * 10^4
    -3 * 10^4 <= nums[i] <= 3 * 10^4
    Each element in the array appears twice except for one element which
    appears only once.
"""


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)


sol = Solution()

print(sol.singleNumber([2, 2, 1]))  # 1

assert sol.singleNumber([2, 2, 1]) == 1
assert sol.singleNumber([4, 1, 2, 1, 2]) == 4
assert sol.singleNumber([1]) == 1

assert sol.singleNumber([0]) == 0
assert sol.singleNumber([-1]) == -1
assert sol.singleNumber([30000]) == 30000
assert sol.singleNumber([-30000]) == -30000

assert sol.singleNumber([0, 1, 1]) == 0
assert sol.singleNumber([1, 1, 0]) == 0
assert sol.singleNumber([1, 0, 1]) == 0
assert sol.singleNumber([5, 5, 0, 0, 3]) == 3

assert sol.singleNumber([2, 1, 2]) == 1
assert sol.singleNumber([1, 2, 3, 2, 1]) == 3
assert sol.singleNumber([7, 3, 5, 3, 7]) == 5
assert sol.singleNumber([4, 4, 9, 9, 1, 1, 8]) == 8
assert sol.singleNumber([8, 1, 1, 9, 9, 4, 4]) == 8

assert sol.singleNumber([-1, -1, -2]) == -2
assert sol.singleNumber([-3, 1, 1]) == -3
assert sol.singleNumber([-5, 5, -5]) == 5
assert sol.singleNumber([-5, 5, 5]) == -5
assert sol.singleNumber([0, -1, -1]) == 0
assert sol.singleNumber([-1, 0, 0]) == -1
assert sol.singleNumber([-2, -3, -2, -4, -4]) == -3

assert sol.singleNumber([30000, 30000, -30000]) == -30000
assert sol.singleNumber([-30000, -30000, 30000]) == 30000
assert sol.singleNumber([30000, -30000, 30000]) == -30000
assert sol.singleNumber([-30000, 0, 30000, 30000, -30000]) == 0

assert sol.singleNumber([1024, 1024, 2048, 4096, 4096]) == 2048
assert sol.singleNumber([3, 3, 3]) == 3
assert sol.singleNumber([2, 2, 2, 2, 2]) == 2

_big = [i for i in range(1, 15000) for _ in range(2)] + [-30000]
assert len(_big) == 29999
assert sol.singleNumber(_big) == -30000

_big_front = [-30000] + [i for i in range(1, 15000) for _ in range(2)]
assert sol.singleNumber(_big_front) == -30000

_interleaved = list(range(1, 15000)) + [30000] + list(range(14999, 0, -1))
assert len(_interleaved) == 29999
assert sol.singleNumber(_interleaved) == 30000