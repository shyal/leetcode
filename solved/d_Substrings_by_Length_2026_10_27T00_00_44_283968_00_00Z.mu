# Given a string s, return every substring of s, grouped by length: every
# substring of length 1 from left to right, then every substring of length
# 2 from left to right, and so on up to s itself. Two substrings that read
# the same but sit at different positions are two entries.
#
# Example 1:
#
# Input: s = "abcd"
# Output: ["a", "b", "c", "d", "ab", "bc", "cd", "abc", "bcd", "abcd"]
# Explanation: the four substrings of length 1, then the three of length
# 2, then the two of length 3, then the one of length 4. Grouping by
# start gives ["a", "ab", "abc", "abcd", "b", ...], which is the wrong
# order here.
#
# Example 2:
#
# Input: s = "aaa"
# Output: ["a", "a", "a", "aa", "aa", "aaa"]
# Explanation: six positions, six entries, three distinct strings.
#
# Example 3:
#
# Input: s = "a"
# Output: ["a"]
#
# Constraints:
#
#     1 <= len(s) <= 100
#     s contains lowercase English letters.
#
#     REQUIRED: len(s) * (len(s) + 1) / 2 entries, one per position, in
#     the stated order. NO set, NO deduplication. The outer loop runs over
#     the length from 1 to len(s); the inner loop runs over the start from
#     0 to len(s) - length.
#
# Note: "shortest first, and stop at the first hit" is the loop of 3076
# and 1062, where the answer is the shortest or longest substring with a
# property. The first substring that passes the test is the answer, and
# the outer loop ends.
#
# ---
# Learning

# mu 0.13

class Solution
  @as_list
  def substringsByLength(s: str) -> [str]
    n = len s
    for size in 1..n
      for start in 0..n - size
        yield s[start:start + size]



sol = Solution()

print(sol.substringsByLength('abcd'))  # ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'abc', 'bcd', 'abcd']

assert sol.substringsByLength('abcd') == ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'abc', 'bcd', 'abcd']
assert sol.substringsByLength('aaa') == ['a', 'a', 'a', 'aa', 'aa', 'aaa']
assert sol.substringsByLength('a') == ['a']
assert sol.substringsByLength('ab') == ['a', 'b', 'ab']
assert sol.substringsByLength('abca') == ['a', 'b', 'c', 'a', 'ab', 'bc', 'ca', 'abc', 'bca', 'abca']
assert len(sol.substringsByLength('abcdefghij')) == 55
assert sol.substringsByLength('abcdefghij')[:10] == list('abcdefghij')
assert sol.substringsByLength('abcdefghij')[-1] == 'abcdefghij'
