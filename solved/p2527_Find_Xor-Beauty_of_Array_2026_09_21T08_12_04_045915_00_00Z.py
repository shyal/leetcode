"""
URL: https://leetcode.com/problems/find-xor-beauty-of-array/description/?envType=problem-list-v2&envId=vn57k9wr

2527. Find Xor-Beauty of Array

You are given a 0-indexed integer array nums.

The effective value of three indices i, j, and k is defined as ((nums[i] | nums[j]) & nums[k]).

The xor-beauty of the array is the XORing of the effective values of all the possible triplets of indices (i, j, k) where 0 <= i, j, k < n.

Return the xor-beauty of nums.

Note that:
- val1 | val2 is bitwise OR of val1 and val2.
- val1 & val2 is bitwise AND of val1 and val2.

Example 1:

Input: nums = [1,4]
Output: 5
Explanation:
The triplets and their corresponding effective values are listed below:
- (0,0,0) with effective value ((1 | 1) & 1) = 1
- (0,0,1) with effective value ((1 | 1) & 4) = 0
- (0,1,0) with effective value ((1 | 4) & 1) = 1
- (0,1,1) with effective value ((1 | 4) & 4) = 4
- (1,0,0) with effective value ((4 | 1) & 1) = 1
- (1,0,1) with effective value ((4 | 1) & 4) = 4
- (1,1,0) with effective value ((4 | 4) & 1) = 0
- (1,1,1) with effective value ((4 | 4) & 4) = 4
Xor-beauty of array will be bitwise XOR of all beauties = 1 ^ 0 ^ 1 ^ 4 ^ 1 ^ 4 ^ 0 ^ 4 = 5.

Example 2:

Input: nums = [15,45,20,2,34,35,5,44,32,30]
Output: 34
Explanation: The xor-beauty of the given array is 34.

Constraints:

    1 <= nums.length < 10^5
    1 <= nums[i] < 10^9

---

LEETCODE: Accepted (3 ms, 33.9 MB)
"""


class Solution:
    def xorBeauty(self, nums: List[int]) -> int:
        return reduce(xor, nums)


sol = Solution()

print(sol.xorBeauty([1, 4]))  # 5

assert sol.xorBeauty([1, 4]) == 5
assert sol.xorBeauty([15, 45, 20, 2, 34, 35, 5, 44, 32, 30]) == 34

assert sol.xorBeauty([0]) == 0
assert sol.xorBeauty([1]) == 1
assert sol.xorBeauty([1, 1, 1]) == 1
assert sol.xorBeauty([2, 2, 2, 2]) == 0
assert sol.xorBeauty([10**9]) == 1000000000
assert sol.xorBeauty([10**9, 10**9]) == 0
assert sol.xorBeauty([10**9, 1, 10**9]) == 1
assert sol.xorBeauty([0, 0, 0, 0]) == 0
assert sol.xorBeauty([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 11
assert sol.xorBeauty([1] * 100000) == 0
assert sol.xorBeauty([i for i in range(1, 100001)]) == 100000
assert sol.xorBeauty([10**9] * 99999 + [1]) == 1000000001
