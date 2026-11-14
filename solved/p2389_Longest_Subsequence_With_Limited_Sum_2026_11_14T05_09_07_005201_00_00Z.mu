# URL: https://leetcode.com/problems/longest-subsequence-with-limited-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2389. Longest Subsequence With Limited Sum
#
# You are given an integer array nums of length n, and an integer array queries of length m.
#
# Return an array answer of length m where answer[i] is the maximum size of a subsequence that you can take from nums such that the sum of its elements is less than or equal to queries[i].
#
# A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.
#
# Example 1:
#
# Input: nums = [4,5,2,1], queries = [3,10,21]
# Output: [2,3,4]
# Explanation: We answer the queries as follows:
# - The subsequence [2,1] has a sum less than or equal to 3. It can be proven that 2 is the maximum size of such a subsequence, so answer[0] = 2.
# - The subsequence [4,5,1] has a sum less than or equal to 10. It can be proven that 3 is the maximum size of such a subsequence, so answer[1] = 3.
# - The subsequence [4,5,2,1] has a sum less than or equal to 21. It can be proven that 4 is the maximum size of such a subsequence, so answer[2] = 4.
#
# Example 2:
#
# Input: nums = [2,3,4,5], queries = [1]
# Output: [0]
# Explanation: The empty subsequence is the only subsequence that has a sum less than or equal to 1, so answer[0] = 0.
#
# Constraints:
#
#     n == nums.length
#     m == queries.length
#     1 <= n, m <= 1000
#     1 <= nums[i], queries[i] <= 10^6
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# we want the maximum size, sort nums incr, precompute prefix sums.
# then iterate over queries, and store the biggest i for which the prefix is <= the query
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# LEETCODE: Accepted (768 ms, 19.3 MB)

# mu 0.18

class Solution
  def answerQueries(nums: [int], queries: [int]) -> [int]
    nums.sort()
    ret res = []
    for q in queries
      best = 0
      for >i, +p in nums
        if p <= q
          best = i + 1
      res <- best


sol = Solution()

print(sol.answerQueries([4, 5, 2, 1], [3, 10, 21]))  # [2,3,4]

assert sol.answerQueries([4, 5, 2, 1], [3, 10, 21]) == [2, 3, 4]
assert sol.answerQueries([2, 3, 4, 5], [1]) == [0]
assert sol.answerQueries([1], [1]) == [1]
assert sol.answerQueries([1], [0]) == [0]
assert sol.answerQueries([10 ** 6] * 1000, [10 ** 6, 10 ** 7, 10 ** 9]) == [1, 10, 1000]
assert sol.answerQueries([1] * 1000, [500, 1000, 1001]) == [500, 1000, 1000]
assert sol.answerQueries([5, 5, 5, 5], [10, 15, 20]) == [2, 3, 4]
assert sol.answerQueries([1, 2, 2, 3, 3, 3], [4, 6, 9]) == [2, 3, 4]
assert sol.answerQueries([10 ** 6], [10 ** 6]) == [1]
assert sol.answerQueries([10 ** 6], [10 ** 5]) == [0]
assert sol.answerQueries([1, 2, 3, 4, 5], [0]) == [0]
assert sol.answerQueries([1, 2, 3, 4, 5], [15]) == [5]
assert sol.answerQueries([1] * 1000, [999, 1000]) == [999, 1000]
assert sol.answerQueries([1000] * 1000, [999999, 1000000]) == [999, 1000]
