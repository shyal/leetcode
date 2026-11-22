# Given an integer array arr, return the length of the longest subsequence
# in arr which is an arithmetic sequence such that the difference between
# adjacent elements in the subsequence equals 1.
#
# A subsequence is a sequence that can be derived from arr by deleting some
# or no elements without changing the order of the remaining elements.
#
# Example 1:
#
# Input: arr = [1, 5, 2, 3, 4]
# Output: 4
# Explanation: The longest arithmetic subsequence is [1, 2, 3, 4].
#
# Example 2:
#
# Input: arr = [4, 3, 2, 1]
# Output: 1
# Explanation: The longest arithmetic subsequence is any single element.
#
# Example 3:
#
# Input: arr = [3, 4, -1, 5, 0, 4, 1, 5, 6]
# Output: 4
# Explanation: The longest arithmetic subsequence is [3, 4, 5, 6].
#
# Constraints:
#
#     1 <= arr.length <= 10^5
#     -10^4 <= arr[i] <= 10^4
#
#     REQUIRED: O(n) time.
#
# ---

# mu 0.20

class Solution
  def longestSubsequence(arr: [int]) -> int
    D = {:int}
    for v in arr
      D[v] = max(D[v-1] + 1, D[v])
    max(D.values())

sol = Solution()

print(sol.longestSubsequence([1, 5, 2, 3, 4]))  # 4

assert sol.longestSubsequence([1, 5, 2, 3, 4]) == 4
assert sol.longestSubsequence([4, 3, 2, 1]) == 1
assert sol.longestSubsequence([3, 4, -1, 5, 0, 4, 1, 5, 6]) == 4
assert sol.longestSubsequence([7]) == 1
assert sol.longestSubsequence([1, 2, 3, 4]) == 4
assert sol.longestSubsequence([1, 3, 5, 7]) == 1
assert sol.longestSubsequence([1, 1, 2, 2, 3]) == 3
assert sol.longestSubsequence([2, 1, 2, 3, 1, 2, 3, 4]) == 4
assert sol.longestSubsequence([-2, -1, 0, 1]) == 4
assert sol.longestSubsequence([5, 5, 5]) == 1
assert sol.longestSubsequence([2, 3, 1, 2, 3]) == 3
assert sol.longestSubsequence([1, 2, 1, 2, 1, 2]) == 2
assert sol.longestSubsequence([10, 1, 11, 2, 12, 3, 13]) == 4
assert sol.longestSubsequence(list(0..<100000)) == 100000
assert sol.longestSubsequence(list(range(100000, 0, -1))) == 1
assert sol.longestSubsequence([1, 2] * 50000) == 2
