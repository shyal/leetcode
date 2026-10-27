# URL: https://leetcode.com/problems/previous-permutation-with-one-swap/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1053. Previous Permutation With One Swap
#
# Given an array of positive integers arr (not necessarily distinct), return the lexicographically largest permutation that is smaller than arr, that can be made with exactly one swap. If it cannot be done, then return the same array.
#
# Note that a swap exchanges the positions of two numbers arr[i] and arr[j].
#
# Example 1:
#
# Input: arr = [3,2,1]
# Output: [3,1,2]
# Explanation: Swapping 2 and 1.
#
# Example 2:
#
# Input: arr = [1,1,5]
# Output: [1,1,5]
# Explanation: This is already the smallest permutation.
#
# Example 3:
#
# Input: arr = [1,9,4,6,7]
# Output: [1,7,4,6,9]
# Explanation: Swapping 9 and 7.
#
# Constraints:
#
#     1 <= arr.length <= 10^4
#     1 <= arr[i] <= 10^4
#
# ---
# if it's a non-decreasing array, it can't be done.
# it looks like the last number always changes
# so let's try all the swaps with the last digit
# and pick the largest swap that's smaller

# mu 0.13

class Solution
  def prevPermOpt1(arr: [int]) -> [int]
    cands = []
    def swap(a, b, arr)
      arr[a], arr[b] = arr[b], arr[a]
      arr
    for i in 0..<len(arr) - 1
      cands <- swap(i, len(arr)-1, arr[::])
    cands.sort(reverse=True)
    res = [cand for cand in cands if cand < arr]
    if res
      return res[0]
    return arr

sol = Solution()

print(sol.prevPermOpt1([3, 2, 1]))  # [3,1,2]

assert sol.prevPermOpt1([3, 2, 1]) == [3, 1, 2]
assert sol.prevPermOpt1([1, 9, 4, 6, 7]) == [1, 7, 4, 6, 9]
assert sol.prevPermOpt1([5, 4, 3, 2, 1]) == [5, 4, 3, 1, 2]
assert sol.prevPermOpt1([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
assert sol.prevPermOpt1([1, 3, 3, 3, 2]) == [1, 3, 3, 2, 3]
assert sol.prevPermOpt1([10 ** 4, 1]) == [1, 10000]
assert sol.prevPermOpt1([2, 3, 1, 1, 1]) == [2, 1, 1, 1, 3]
assert sol.prevPermOpt1([1, 1, 1, 1, 2]) == [1, 1, 1, 1, 2]
assert sol.prevPermOpt1([3, 1, 1, 1, 1]) == [1, 1, 1, 1, 3]
assert sol.prevPermOpt1([1, 2, 3, 4, 3, 2, 1]) == [1, 2, 3, 4, 3, 1, 2]
assert sol.prevPermOpt1([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert sol.prevPermOpt1([1, 1, 5]) == [1, 1, 5]
assert sol.prevPermOpt1([1]) == [1]
assert sol.prevPermOpt1([2, 2, 2, 2]) == [2, 2, 2, 2]
