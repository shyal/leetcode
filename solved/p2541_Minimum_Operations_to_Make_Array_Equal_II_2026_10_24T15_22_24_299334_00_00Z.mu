# URL: https://leetcode.com/problems/minimum-operations-to-make-array-equal-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2541. Minimum Operations to Make Array Equal II
#
# You are given two integer arrays nums1 and nums2 of equal length n and an integer k. You can perform the following operation on nums1:
#
# - Choose two indexes i and j and increment nums1[i] by k and decrement nums1[j] by k. In other words, nums1[i] = nums1[i] + k and nums1[j] = nums1[j] - k.
#
# nums1 is said to be equal to nums2 if for all indices i such that 0 <= i < n, nums1[i] == nums2[i].
#
# Return the minimum number of operations required to make nums1 equal to nums2. If it is impossible to make them equal, return -1.
#
# Example 1:
#
# Input: nums1 = [4,3,1,4], nums2 = [1,3,7,1], k = 3
# Output: 2
# Explanation: In 2 operations, we can transform nums1 to nums2.
# 1st operation: i = 2, j = 0. After applying the operation, nums1 = [1,3,4,4].
# 2nd operation: i = 2, j = 3. After applying the operation, nums1 = [1,3,7,1].
# One can prove that it is impossible to make arrays equal in fewer operations.
#
# Example 2:
#
# Input: nums1 = [3,8,5,2], nums2 = [2,4,1,6], k = 1
# Output: -1
# Explanation: It can be proved that it is impossible to make the two arrays equal.
#
# Constraints:
#
#     n == nums1.length == nums2.length
#     2 <= n <= 10^5
#     0 <= nums1[i], nums2[j] <= 10^9
#     0 <= k <= 10^5
#
# ---
# LEETCODE: Accepted (710 ms, 38.3 MB)

# mu 0.12

class Solution
  def minOperations(nums1: [int], nums2: [int], k: int) -> int
    if k == 0
      if any([a != b for a, b in zip(nums1, nums2)]) 
        return -1
      else
        return 0
    if any(abs(a - b) % k != 0 for a, b in zip(nums1, nums2))
      return -1
    diffs = [a - b for a, b in zip(nums1, nums2)]
    keep = [a != b for a, b in zip(nums1, nums2)]
    nums1 = [x for >i, x in nums1 if keep[i]]
    nums2 = [x for >i, x in nums2 if keep[i]]
    pos = heap([x for x in diffs if x > 0], type=min)
    neg = heap([x for x in diffs if x < 0], type=max)
    ops = 0
    while pos and neg
      a = pos.pop()
      b = - neg.pop()
      least = min(a // k, b // k)
      ops += least
      a -= k * least
      b -= k * least
      if a
        pos.push(a)
      if b
        neg.push(-b)
    if not pos and not neg
      return ops
    -1

sol = Solution()

print(sol.minOperations([4, 3, 1, 4], [1, 3, 7, 1], 3))  # 2

assert sol.minOperations([4, 3, 1, 4], [1, 3, 7, 1], 3) == 2
assert sol.minOperations([3, 8, 5, 2], [2, 4, 1, 6], 1) == -1
assert sol.minOperations([1, 1], [1, 1], 0) == 0
assert sol.minOperations([1, 2], [2, 1], 0) == -1
assert sol.minOperations([0, 0, 0], [0, 0, 0], 5) == 0
assert sol.minOperations([10 ** 9, 10 ** 9], [10 ** 9, 10 ** 9], 1) == 0
assert sol.minOperations([10 ** 9, 0], [0, 10 ** 9], 10 ** 5) == 10000
assert sol.minOperations([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 1) == 6
assert sol.minOperations([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 2) == 3
assert sol.minOperations([1, 1, 1, 1], [1, 1, 1, 2], 1) == -1
assert sol.minOperations([5, 5, 5, 5], [5, 5, 5, 5], 0) == 0
assert sol.minOperations([1, 1, 1, 1], [1, 1, 1, 1], 1) == 0
assert sol.minOperations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 1) == 25
assert sol.minOperations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 3) == -1
