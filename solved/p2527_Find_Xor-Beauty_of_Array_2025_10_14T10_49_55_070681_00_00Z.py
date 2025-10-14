"""
URL: https://leetcode.com/problems/find-xor-beauty-of-array/description/

2527. Find Xor-Beauty of Array

You are given a 0-indexed integer array nums.

The effective value of three indices i, j, and k is defined as ((nums[i] | nums[j]) & nums[k]).

The xor-beauty of the array is the XORing of the effective values of all the possible triplets of indices (i, j, k) where 0 <= i, j, k < n.

Return the xor-beauty of nums.

Note that:

        val1 | val2 is bitwise OR of val1 and val2.
        val1 & val2 is bitwise AND of val1 and val2.


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

        1 <= nums.length <= 105
        1 <= nums[i] <= 109

---

Ok so i could brute force this one, but then TLE. I tried following the hints,
but was stumped.

Looking at solutions.. someone in discussion said "just xor the array" which indeed works.

Will need to revisit:

https://leetcode.com/problems/find-xor-beauty-of-array/solutions/3014972/python3-one-liner-with-formal-proof/

I totally understand the proof. But making the leap triplet combinations to discarding unnecessary computations
still feels like a big leap.
"""


class Solution:
    def xorBeautyBruteForce(self, nums: List[int]) -> int:
        effective = lambda i, j, k: ((nums[i] | nums[j]) & nums[k])
        return reduce(
            ixor,
            starmap(
                effective, product(range(len(nums)), range(len(nums)), range(len(nums)))
            ),
        )

    def xorBeautyBruteForce2(self, nums: List[int]) -> int:
        effective = lambda i, k: (nums[i] & nums[k])
        return reduce(
            ixor,
            starmap(effective, product(range(len(nums)), range(len(nums)))),
        )

    def xorBeauty(self, nums: List[int]) -> int:
        return reduce(ixor, nums)


sol = Solution()

assert sol.xorBeauty(nums=[1, 4]) == 5
assert sol.xorBeauty(nums=[15, 45, 20, 2, 34, 35, 5, 44, 32, 30]) == 34
assert sol.xorBeautyBruteForce(nums=[15, 45, 20, 2, 34, 35, 5, 44, 32, 30]) == 34
assert sol.xorBeautyBruteForce2(nums=[15, 45, 20, 2, 34, 35, 5, 44, 32, 30]) == 34
assert sol.xorBeauty(nums=([1] * int(10e5))) == 0
