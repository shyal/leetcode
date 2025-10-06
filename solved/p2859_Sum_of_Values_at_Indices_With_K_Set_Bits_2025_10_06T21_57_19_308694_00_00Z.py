"""
URL: https://leetcode.com/problems/sum-of-values-at-indices-with-k-set-bits/description/?envType=daily-question&envId=2024-09-18

2859. Sum of Values at Indices With K Set Bits

You are given a 0-indexed integer array nums and an integer k.

Return an integer that denotes the sum of elements in nums whose corresponding indices have exactly k set bits in their binary representation.

The set bits of an integer are the 1's present when it is written in binary.

    For example, the binary representation of 21 is 10101, which has 3 set bits.


Example 1:

Input: nums = [5,10,1,5,2], k = 1
Output: 13
Explanation: The binary representation of the indices are:
0 is 0 in binary, 0 set bits
1 is 1 in binary, 1 set bits
2 is 10 in binary, 1 set bits
3 is 11 in binary, 2 set bits
4 is 100 in binary, 1 set bits
Indices 1,2,4 have one set bit and their sum is 10 + 1 + 2 = 13.

Example 2:

Input: nums = [4,3,2,1], k = 2
Output: 1
Explanation: The binary representation of the indices are:
0 is 0 in binary, 0 set bits
1 is 1 in binary, 1 set bits
2 is 10 in binary, 1 set bits
3 is 11 in binary, 2 set bits
Only index 3 has two set bits and its value is 1.


Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i] <= 105
    0 <= k <= 10

"""


class Solution:

    def count_bits(self, n):
        count = 0
        while n:
            count += 1
            n &= n - 1
        return count

    def sumIndicesWithKSetBits(self, nums: List[int], k: int) -> int:
        count = 0
        for i, n in enumerate(nums):
            bits = self.count_bits(i)
            if bits == k:
                count += n
        return count


sol = Solution()

assert sol.sumIndicesWithKSetBits([5, 10, 1, 5, 2], 1) == 13
assert sol.sumIndicesWithKSetBits([4, 3, 2, 1], 2) == 1
assert sol.sumIndicesWithKSetBits([1], 0) == 1
assert sol.sumIndicesWithKSetBits([1], 1) == 0
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 0
    )
    == 1
)
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 1
    )
    == 19
)
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 2
    )
    == 51
)
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 3
    )
    == 49
)
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 4
    )
    == 16
)
assert (
    sol.sumIndicesWithKSetBits(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 5
    )
    == 0
)
assert sol.sumIndicesWithKSetBits([1] * 16, 10) == 0
