# URL: https://leetcode.com/problems/number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1577. Number of Ways Where Square of Number Is Equal to Product of Two Numbers
#
# Given two arrays of integers nums1 and nums2, return the number of triplets formed (type 1 and type 2) under the following rules:
#
# - Type 1: Triplet (i, j, k) if nums1[i]^2 == nums2[j] * nums2[k] where 0 <= i < nums1.length and 0 <= j < k < nums2.length.
# - Type 2: Triplet (i, j, k) if nums2[i]^2 == nums1[j] * nums1[k] where 0 <= i < nums2.length and 0 <= j < k < nums1.length.
#
# Example 1:
#
# Input: nums1 = [7,4], nums2 = [5,2,8,9]
# Output: 1
# Explanation: Type 1: (1, 1, 2), nums1[1]^2 = nums2[1] * nums2[2]. (4^2 = 2 * 8).
#
# Example 2:
#
# Input: nums1 = [1,1], nums2 = [1,1,1]
# Output: 9
# Explanation: All Triplets are valid, because 1^2 = 1 * 1.
# Type 1: (0,0,1), (0,0,2), (0,1,2), (1,0,1), (1,0,2), (1,1,2).  nums1[i]^2 = nums2[j] * nums2[k].
# Type 2: (0,0,1), (1,0,1), (2,0,1). nums2[i]^2 = nums1[j] * nums1[k].
#
# Example 3:
#
# Input: nums1 = [7,7,8,3], nums2 = [1,2,9,7]
# Output: 2
# Explanation: There are 2 valid triplets.
# Type 1: (3,0,2).  nums1[3]^2 = nums2[0] * nums2[2].
# Type 2: (3,0,1).  nums2[3]^2 = nums1[0] * nums1[1].
#
# Constraints:
#
#     1 <= nums1.length, nums2.length <= 1000
#     1 <= nums1[i], nums2[i] <= 10^5
#
# ---
# 
# brute force solution:
# 
# class Solution
#   def numTriplets(nums1: [int], nums2: [int]) -> int
#     ret res = 0
#     for i in 0..<len(nums1)
#       for j in 0..<len(nums2)
#         for k in j+1..<len(nums2)
#           type1 = nums1[i] ** 2 == nums2[j] * nums2[k]
#           res += type1
#     for i in 0..<len(nums2)
#       for j in 0..<len(nums1)
#         for k in j+1..<len(nums1)
#           type2 = nums2[i] ** 2 == nums1[j] * nums1[k]
#           res += type2
#
# 
# mu 0.18
# solved, but heavily hinted
# LEETCODE: Accepted (818 ms, 19 MB)

class Solution
  def numTriplets(nums1: [int], nums2: [int]) -> int
    ret res = 0
    for i in 0..<len(nums1)
      D2 = {:int}
      for j in 0..<len(nums2)
        comp, rem = divmod(nums1[i] ** 2, nums2[j])
        if not rem
          res += D2[comp]
        D2[nums2[j]] += 1
    for i in 0..<len(nums2)
      D1 = {:int}
      for j in 0..<len(nums1)
        comp, rem = divmod(nums2[i] ** 2, nums1[j])
        if not rem
          res += D1[comp]
        D1[nums1[j]] += 1

sol = Solution()

print(sol.numTriplets([7, 4], [5, 2, 8, 9]))  # 1

assert sol.numTriplets([7, 4], [5, 2, 8, 9]) == 1
assert sol.numTriplets([1, 1], [1, 1, 1]) == 9
assert sol.numTriplets([7, 7, 8, 3], [1, 2, 9, 7]) == 2

assert sol.numTriplets([1], [1]) == 0
assert sol.numTriplets([10 ** 5], [10 ** 5]) == 0
assert sol.numTriplets([2, 2, 2], [4, 4, 4]) == 0
assert sol.numTriplets([3, 3, 3], [9, 9, 9]) == 0
assert sol.numTriplets([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]) == 4
assert sol.numTriplets([10 ** 5] * 1000, [10 ** 5] * 1000) == 999000000
assert sol.numTriplets([1, 1, 1, 1], [1, 1]) == 16
assert sol.numTriplets([2, 3, 5, 7], [11, 13, 17, 19]) == 0
assert sol.numTriplets([2, 4, 8, 16], [1, 2, 4, 8]) == 4
assert sol.numTriplets([1, 1, 2, 2], [1, 2, 2, 4]) == 7
assert sol.numTriplets([1, 3, 9, 27], [1, 3, 9, 27]) == 4
