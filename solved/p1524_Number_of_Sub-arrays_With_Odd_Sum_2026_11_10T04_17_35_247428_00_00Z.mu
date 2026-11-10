# URL: https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1524. Number of Sub-arrays With Odd Sum
#
# Given an array of integers arr, return the number of subarrays with an odd sum.
#
# Since the answer can be very large, return it modulo 10^9 + 7.
#
# Example 1:
#
# Input: arr = [1,3,5]
# Output: 4
# Explanation: All subarrays are [[1],[1,3],[1,3,5],[3],[3,5],[5]]
# All sub-arrays sum are [1,4,9,3,8,5].
# Odd sums are [1,9,3,5] so the answer is 4.
#
# Example 2:
#
# Input: arr = [2,4,6]
# Output: 0
# Explanation: All subarrays are [[2],[2,4],[2,4,6],[4],[4,6],[6]]
# All sub-arrays sum are [2,6,12,4,10,6].
# All sub-arrays have even sum and the answer is 0.
#
# Example 3:
#
# Input: arr = [1,2,3,4,5,6,7]
# Output: 16
#
# Constraints:
#
#     1 <= arr.length <= 10^5
#     1 <= arr[i] <= 100
#
# ---
# 
# O(n**3) version:
# 
# class Solution
#   def numOfSubarrays(arr: [int]) -> int
#     n = len arr
#     count = 0
#     for i in 0..<n
#       for j in i..<n
#         sa = arr[i:j+1]
#         if sum(sa) is odd
#           count += 1
#     count % (10**9 + 7)
# 
# O(n**2) version:
# 
# class Solution
#   def numOfSubarrays(arr: [int]) -> int
#     n = len arr
#     count = 0
#     for i in 0..<n
#       prefix = 0
#       for j in i..<n
#         prefix += arr[j]
#         if prefix is odd
#           count += 1
#     count % (10**9 + 7)
# 
# 
# Solved the brute force versions, but not the version below. learning.

class Solution
  def numOfSubarrays(arr: [int]) -> int
    oddc = 0
    for prefix in scan(+, arr)
      oddc += prefix is odd
    evenc = len arr - oddc + 1
    (oddc * evenc) % (10**9 + 7)


sol = Solution()

print(sol.numOfSubarrays([1, 3, 5]))  # 4

assert sol.numOfSubarrays([1, 3, 5]) == 4
assert sol.numOfSubarrays([2, 4, 6]) == 0
assert sol.numOfSubarrays([1, 2, 3, 4, 5, 6, 7]) == 16
assert sol.numOfSubarrays([1]) == 1
assert sol.numOfSubarrays([2]) == 0
assert sol.numOfSubarrays([1, 1, 1, 1, 1]) == 9
assert sol.numOfSubarrays([2, 2, 2, 2, 2]) == 0
assert sol.numOfSubarrays([1, 2, 1, 2, 1, 2]) == 12
assert sol.numOfSubarrays([-1, -3, -5]) == 4
assert sol.numOfSubarrays([100] * 10 ** 5) == 0
assert sol.numOfSubarrays([1] * 10 ** 5) == 500049986
assert sol.numOfSubarrays([1, 2] * 50000) == 500049986
assert sol.numOfSubarrays([0]) == 0
assert sol.numOfSubarrays([0, 0, 0, 0]) == 0
assert sol.numOfSubarrays([1, 100, 1, 100, 1]) == 9
