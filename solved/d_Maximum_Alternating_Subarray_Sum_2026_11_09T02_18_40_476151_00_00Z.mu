# Given an integer array nums, return the largest alternating sum of a
# non-empty subarray. The alternating sum of a subarray is its first
# element minus its second plus its third, and so on: the elements at even
# positions in the subarray are added, the elements at odd positions are
# subtracted.
#
# Example 1:
#
# Input: nums = [1, 2, 3]
# Output: 3
# Explanation: the subarray [3]; the whole array gives 1 - 2 + 3 = 2.
#
# Example 2:
#
# Input: nums = [1, -5]
# Output: 6
# Explanation: the whole array, 1 - (-5); the answer ends on a subtracted
# element.
#
# Example 3:
#
# Input: nums = [2, 5, 1, 4]
# Output: 8
# Explanation: the subarray [5, 1, 4], 5 - 1 + 4.
#
# Constraints:
#
#     1 <= len(nums) <= 10^5
#     -10^5 <= nums[i] <= 10^5
#
#     REQUIRED: O(n) time, O(1) extra space, a single pass. NO enumeration
#     of subarrays. The empty subarray is not allowed.
#
# ---
# Learning

# mu 0.16

def sign(s: int) -> str
  s == 1 ? "+" : "-"

def viz(nums)
  n = len nums
  G = {}      # the decision tree: node -> its two choices
  value = {}  # node -> the best leaf below it
  # the node "nums[i] with sign s": stop here, or take nums[i + 1] with -s
  memo best(i, s)
    node = f"{sign(s)}{nums[i]} @{i}"
    stop = f"stop @{i}{sign(s)}"
    G[node] = [stop]
    value[stop] = 0
    cont = -inf
    if i + 1 < n
      G[node] <- f"{sign(-s)}{nums[i + 1]} @{i + 1}"
      cont = best(i + 1, -s)
    value[node] = s * nums[i] + max(0, cont)
    return value[node]
  answer = max for i in range n: best(i, 1)
  draw_graphviz(G, directed=true, labels=value)
  answer

class Solution
  def maxAlternatingSum(nums: [int]) -> int
    n = len nums
    memo best(i, s) = 
      | i == n  -> -inf
      | else    -> s * nums[i] + max(0, best(i + 1, -s))
    max for i in 0..<n: best(i, 1)

sol = Solution()

print(sol.maxAlternatingSum([1, 2, 3, 4, 5]))  # 3

assert sol.maxAlternatingSum([1, 2, 3]) == 3
assert sol.maxAlternatingSum([1, -5]) == 6
assert sol.maxAlternatingSum([2, 5, 1, 4]) == 8
assert sol.maxAlternatingSum([5, -5, 1]) == 11
assert sol.maxAlternatingSum([4, 7]) == 7
assert sol.maxAlternatingSum([-72]) == -72
assert sol.maxAlternatingSum([-5, -5]) == 0
assert sol.maxAlternatingSum([1, -1, 1, -1, 1]) == 5
assert sol.maxAlternatingSum([9, 1, 1, 1, 1, 1, 1, 1]) == 9
assert sol.maxAlternatingSum([1, 1, 1, 1, 1, 1, 1, 9]) == 9
assert sol.maxAlternatingSum([1, 1, 1, 9, 1, 1, 1, 1]) == 9
assert sol.maxAlternatingSum([2, -3, 2, -3, 2, -3, 2, -3]) == 20
assert sol.maxAlternatingSum([1, -1] * 50000) == 100000
assert sol.maxAlternatingSum([10 ** 5] * 10 ** 5) == 10 ** 5
assert sol.maxAlternatingSum([-10 ** 5] * 10 ** 5) == 0
