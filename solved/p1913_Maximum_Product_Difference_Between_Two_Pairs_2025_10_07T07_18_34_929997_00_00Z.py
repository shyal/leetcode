"""
URL: https://leetcode.com/problems/maximum-product-difference-between-two-pairs/description/

1913. Maximum Product Difference Between Two Pairs

The product difference between two pairs (a, b) and (c, d) is defined as (a * b) - (c * d).

Choose four distinct indices i, j, k, l such that 0 <= i, j, k, l < nums.length. You can pair them up as (nums[i], nums[j]) and (nums[k], nums[l]) in such a way that the product difference is maximized.

Return the maximum such product difference.


Example 1:

Input: nums = [5,6,2,7,4]
Output: 34
Explanation: Consider the pairs (nums[1], nums[3]) = (6, 7) and (nums[2], nums[4]) = (2, 4)
(6 * 7) - (2 * 4) = 42 - 8 = 34

Example 2:

Input: nums = [4,2,5,9,7,4,8]
Output: 64
Explanation: Consider the pairs (nums[3], nums[6]) = (9, 8) and (nums[1], nums[0]) = (2, 4)
(9 * 8) - (2 * 4) = 72 - 8 = 64


Constraints:

    4 <= nums.length <= 10^4
    1 <= nums[i] <= 10^4

---

brute force permutations works, but hits TLE. Need more optimal approach.

[5, 6, 2, 7, 4]

since we want to maximize the result, we should pick the largest values for a and b,
and the smallest for c and d.

"""


class Solution:
    def maxProductDifferenceBruteForce(self, nums: List[int]) -> int:
        return max((a * b) - (c * d) for a, b, c, d in permutations(nums, 4))

    def maxProductDifference(self, nums: List[int]) -> int:
        nums.sort()
        n = nums
        return n[-1] * n[-2] - n[0] * n[1]


sol = Solution()

TLE = [
    5024,
    4119,
    3778,
    1977,
    3156,
    5170,
    1959,
    8780,
    3034,
    3139,
    3546,
    7934,
    4531,
    9660,
    8596,
    9778,
    4637,
    1648,
    3181,
    4854,
    3728,
    5913,
    2940,
    4953,
    232,
    8752,
    2074,
    4495,
    746,
    894,
    1730,
    7103,
    5935,
    7533,
    2507,
    7136,
    2886,
    8549,
    4426,
    8818,
    7922,
    7617,
    7137,
    9708,
    4398,
    5281,
    4023,
    1420,
    4570,
    7386,
    3996,
    7614,
    9337,
    10000,
    6210,
    5512,
    471,
    8099,
    5326,
    2980,
    7989,
    3476,
    5814,
    4233,
    5577,
    4582,
    9768,
    4527,
    9107,
    167,
    8465,
    3131,
    1403,
    3955,
    6659,
    8005,
    9097,
    3938,
    7801,
    8042,
    7343,
    283,
    1525,
    4821,
    3631,
    6626,
    3987,
    5017,
    9529,
    6047,
    7754,
    9069,
    8699,
    5633,
    6972,
    9018,
    5420,
    5765,
    7435,
    4439,
]

assert sol.maxProductDifference(TLE) == 97741256
assert sol.maxProductDifference([5, 6, 2, 7, 4]) == 34
assert sol.maxProductDifference([4, 2, 5, 9, 7, 4, 8]) == 64
assert sol.maxProductDifference([1, 2, 3, 4]) == 10
assert sol.maxProductDifference([5, 5, 5, 5]) == 0
assert sol.maxProductDifference([1, 1, 2, 3]) == 5
assert sol.maxProductDifference([1, 1, 10000, 10000]) == 99999999
assert sol.maxProductDifference([1, 2, 3, 100]) == 298
assert sol.maxProductDifference([1, 10000, 1, 10000]) == 99999999
assert sol.maxProductDifference([4, 4, 4, 4, 4]) == 0
assert sol.maxProductDifference([1, 3, 2, 4, 5, 6]) == (6 * 5) - (1 * 2)
