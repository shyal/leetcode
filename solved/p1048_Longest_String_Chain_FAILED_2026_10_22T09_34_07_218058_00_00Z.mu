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
# Hint: a word has 16 letters or fewer. To get each possible predecessor of words[i], you remove one letter. How many possible predecessors are there, and how can you find out quickly if one of them is in words?
# LEETCODE: Time Limit Exceeded (78/86 cases)

# mu 0.12

class Solution

  memo is_pred(A, B)
    len(A) == len(B) -1 and lcs(A, B) == len(A)

  def longestStrChain(words: [str]) -> int
    words.sort(key=x -> len(x))
    dp = table(len(words), fill=1)
    self.is_pred('BCA', "BDCA")
    for j, i in pairs(len(words), back=true)
      if len(words[j]) == len(words[i]) -1 and self.is_pred(words[j], words[i])
        dp[i] = max(dp[j] + 1, dp[i])
    max(dp)

sol = Solution()



# assert sol.is_pred("ab",  "bac") == False
assert sol.is_pred('ABC', 'ABCD') == True
assert sol.is_pred('ABC', 'ABC') == False
assert sol.is_pred('ABC', 'ADBC') == True
assert sol.is_pred('ABC', 'DBCD') == False

assert sol.longestStrChain(['abcd', 'dbqca']) == 1
assert sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca']) == 4
sol.longestStrChain(['xbc', 'pcxbcf', 'xb', 'cxbc', 'pcxbc']) == 5
assert sol.longestStrChain(['xbc', 'pcxbcf', 'xb', 'cxbc', 'pcxbc']) == 5

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


# FAILED: walked away after 56m 53s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
