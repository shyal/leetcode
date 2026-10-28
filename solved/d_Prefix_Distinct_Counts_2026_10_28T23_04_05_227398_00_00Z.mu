# Given a string s, return a list with one integer per index: the integer
# at index i is the number of distinct letters in s[:i + 1]. Walk s from
# the left, add each letter to the set of letters seen so far, and record
# the size of the set. For example with s = "abbcbc", after "a" the size
# is 1, after "ab" it is 2, after "abb" it is still 2, after "abbc" it is
# 3, and it stays 3 to the end.
#
# Example 1:
#
# Input: s = "abbcbc"
# Output: [1, 2, 2, 3, 3, 3]
#
# Example 2:
#
# Input: s = "zqq"
# Output: [1, 2, 2]
#
# Example 3:
#
# Input: s = "a"
# Output: [1]
#
# Constraints:
#
#     1 <= len(s) <= 2000
#     s contains lowercase English letters.
#
#     REQUIRED: one pass over s. NO len(set(s[:i + 1])) per index:
#     rebuilding each prefix from scratch is quadratic and is the failure
#     mode this drill exists to kill.
#
# This is the size of each set of d312 Prefix Letter Sets.
#
# ---

# mu 0.13

# mu 0.13

class Solution
  def prefixDistinctCounts(s: str) -> [int]
    [len(y) for y in scan(set.union, [set(x) for x in s])]

sol = Solution()

print(sol.prefixDistinctCounts('abbcbc'))  # [1, 2, 2, 3, 3, 3]

assert sol.prefixDistinctCounts('abbcbc') == [1, 2, 2, 3, 3, 3]
assert sol.prefixDistinctCounts('zqq') == [1, 2, 2]
assert sol.prefixDistinctCounts('a') == [1]
assert sol.prefixDistinctCounts('aaaa') == [1, 1, 1, 1]
assert sol.prefixDistinctCounts('abcd') == [1, 2, 3, 4]
assert sol.prefixDistinctCounts('ab' * 1000) == [1] + [2] * 1999
