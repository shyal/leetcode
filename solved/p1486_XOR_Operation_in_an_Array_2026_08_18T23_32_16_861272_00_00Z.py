"""
URL: https://leetcode.com/problems/xor-operation-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

1486. XOR Operation in an Array

You are given an integer n and an integer start.

Define an array nums where nums[i] = start + 2 * i (0-indexed) and n == nums.length.

Return the bitwise XOR of all elements of nums.


Example 1:

Input: n = 5, start = 0
Output: 8
Explanation: Array nums is equal to [0, 2, 4, 6, 8] where (0 ^ 2 ^ 4 ^ 6 ^ 8) = 8.
Where "^" corresponds to bitwise XOR operator.

Example 2:

Input: n = 4, start = 3
Output: 8
Explanation: Array nums is equal to [3, 5, 7, 9] where (3 ^ 5 ^ 7 ^ 9) = 8.


Constraints:

    1 <= n <= 1000
    0 <= start <= 1000
    n == nums.length
"""


class Solution:
    def xorOperation(self, n: int, start: int) -> int:
        nums = [start + 2 * i for i in range(n)]
        return reduce(xor, nums)


sol = Solution()

print(sol.xorOperation(5, 0))  # 8

assert sol.xorOperation(5, 0) == 8
assert sol.xorOperation(4, 3) == 8
assert sol.xorOperation(1, 0) == 0
assert sol.xorOperation(1, 7) == 7
assert sol.xorOperation(1, 1000) == 1000
assert sol.xorOperation(2, 0) == 2
assert sol.xorOperation(2, 5) == 2
assert sol.xorOperation(3, 1) == 7
assert sol.xorOperation(5, 1) == 9
assert sol.xorOperation(6, 3) == 14
assert sol.xorOperation(7, 2) == 0
assert sol.xorOperation(8, 1) == 0
assert sol.xorOperation(10, 5) == 2
assert sol.xorOperation(3, 1000) == 1006
assert sol.xorOperation(1000, 0) == 0
assert sol.xorOperation(1000, 1000) == 0