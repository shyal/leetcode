# URL: https://leetcode.com/problems/longest-string-chain/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1048. Longest String Chain
#
# You are given an array of words where each word consists of lowercase English letters.
#
# word_A is a predecessor of word_B if and only if we can insert exactly one letter anywhere in word_A without changing the order of the other characters to make it equal to word_B.
#
# For example, "abc" is a predecessor of "abac", while "cba" is not a predecessor of "bcad".
#
# A word chain is a sequence of words [word_1, word_2, ..., word_k] with k >= 1, where word_1 is a predecessor of word_2, word_2 is a predecessor of word_3, and so on. A single word is trivially a word chain with k == 1.
#
# Return the length of the longest possible word chain with words chosen from the given list of words.
#
# Example 1:
#
# Input: words = ["a","b","ba","bca","bda","bdca"]
# Output: 4
# Explanation: One of the longest word chains is ["a","ba","bda","bdca"].
#
# Example 2:
#
# Input: words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]
# Output: 5
# Explanation: All the words can be put in a word chain ["xb", "xbc", "cxbc", "pcxbc", "pcxbcf"].
#
# Example 3:
#
# Input: words = ["abcd","dbqca"]
# Output: 1
# Explanation: The trivial word chain ["abcd"] is one of the longest word chains.
# ["abcd","dbqca"] is not a valid word chain because the ordering of the letters is changed.
#
# Constraints:
#
#     1 <= words.length <= 1000
#     1 <= words[i].length <= 16
#     words[i] only consists of lowercase English letters.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# sort words by length (longest to shortest)
# create a words set, e.g wordss
# for every item in words, generate variations that are one letter shorter, e.g
#   bdca -> dca bca bda bdc
#     for each of those, check if they're in wordss
#       if it is in that one, then recursively proceed to check
#       if shorter versions are in the array etc
#       the max depth of the recursion is the longest chain of predecessors
# the recursive function uses caching
# 
# STAGE 1: miss (recognition failure, slow)
# STAGE 1: miss (recognition failure, slow)
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# 
# 
# 
# 
# LEETCODE: Accepted (1752 ms, 31.3 MB)

# mu 0.20

class Solution
  def longestStrChain(words: [str]) -> int
    wordss = set(words)
    words.sort(key=len, reverse=true)
    memo best(word, depth)
      best_depth = depth
      for j in 0..<len(word)
        var = word[:j] + word[j+1:]
        if var in words
          best_depth = max(best_depth, best(var, depth + 1))
      return best_depth
    max for words: best(_, 1)


sol = Solution()

print(sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca']))  # 4

assert sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca']) == 4
assert sol.longestStrChain(['xbc', 'pcxbcf', 'xb', 'cxbc', 'pcxbc']) == 5
assert sol.longestStrChain(['abcd', 'dbqca']) == 1
assert sol.longestStrChain(['a']) == 1
assert sol.longestStrChain(['a', 'aa', 'aaa', 'aaaa', 'aaaaa']) == 5
assert sol.longestStrChain(['a', 'b', 'c', 'd']) == 1
assert sol.longestStrChain(['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef']) == 6
assert sol.longestStrChain(['a', 'ab', 'ac', 'abc', 'abd', 'abcd', 'abce']) == 4
assert sol.longestStrChain(['z' * i for i in 1..<17]) == 16
assert sol.longestStrChain(['a' * 16, 'a' * 15, 'a' * 14]) == 3
assert sol.longestStrChain(['a', 'ab', 'abc', 'abd', 'abdd', 'abddd', 'abdddd']) == 6
assert sol.longestStrChain(['a', 'ba', 'bca', 'bdca', 'bdcaa']) == 5
assert sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca', 'bdcaa', 'bdcaaa']) == 6
assert sol.longestStrChain(['a' * i for i in 1..<1001 if i <= 16]) == 16
assert sol.longestStrChain(['a' * 16] * 1000) == 1
