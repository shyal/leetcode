# URL: https://leetcode.com/problems/shortest-uncommon-substring-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3076. Shortest Uncommon Substring in an Array
#
# You are given an array arr of size n consisting of non-empty strings.
#
# Find a string array answer of size n such that:
#
# - answer[i] is the shortest substring of arr[i] that does not occur as a substring in any other string in arr. If multiple such substrings exist, answer[i] should be the lexicographically smallest. And if no such substring exists, answer[i] should be an empty string.
#
# Return the array answer.
#
# Example 1:
#
# Input: arr = ["cab","ad","bad","c"]
# Output: ["ab","","ba",""]
# Explanation: We have the following:
# - For the string "cab", the shortest substring that does not occur in any other string is either "ca" or "ab", we choose the lexicographically smaller substring, which is "ab".
# - For the string "ad", there is no substring that does not occur in any other string.
# - For the string "bad", the shortest substring that does not occur in any other string is "ba".
# - For the string "c", there is no substring that does not occur in any other string.
#
# Example 2:
#
# Input: arr = ["abc","bcd","abcd"]
# Output: ["","","abcd"]
# Explanation: We have the following:
# - For the string "abc", there is no substring that does not occur in any other string.
# - For the string "bcd", there is no substring that does not occur in any other string.
# - For the string "abcd", the shortest substring that does not occur in any other string is "abcd".
#
# Constraints:
#
#     n == arr.length
#     2 <= n <= 100
#     1 <= arr[i].length <= 20
#     arr[i] consists only of lowercase English letters.
#
# ---
# LEETCODE: Accepted (224 ms, 19.2 MB)

# mu 0.13

class Solution
  def shortestSubstrings(arr: [str]) -> [str]
    def ss_in_array(ss, skip)
      any(ss in x if i != skip else false for >i, x in arr)
    def shortest(ind)
      cand = ''
      n = len(arr[ind])
      for size in 1..n
        for i in 0..n - size
          ss = arr[ind][i:i + size]
          if not ss_in_array(ss, ind)
            if (cand and ss < cand) or cand == ''
              cand = ss
        if cand
          break
      if cand
        return cand
      ''
    [shortest(i) for i in 0..<len arr]

sol = Solution()
print(sol.shortestSubstrings(['cab', 'ad', 'bad', 'c']))  # ["ab","","ba",""]
assert sol.shortestSubstrings(['cab', 'ad', 'bad', 'c']) == ['ab', '', 'ba', '']
assert sol.shortestSubstrings(['abc', 'bcd', 'abcd']) == ['', '', 'abcd']
assert sol.shortestSubstrings(['a', 'a']) == ['', '']
assert sol.shortestSubstrings(['abc', 'abc', 'abc']) == ['', '', '']
assert sol.shortestSubstrings(['abc', 'def', 'ghi']) == ['a', 'd', 'g']
assert sol.shortestSubstrings(['aaaaa', 'aaa', 'aa']) == ['aaaa', '', '']
assert sol.shortestSubstrings(['abcde' * 4, 'bcdea' * 4, 'cdeab' * 4]) == ['abcdeabcdeabcdeabc', 'bcdeabcdeabcdeabcdea', 'eabcdeabcdeabcdeab']
assert sol.shortestSubstrings(['a' * 20, 'b' * 20]) == ['a', 'b']
assert sol.shortestSubstrings(['abc', 'ab', 'a']) == ['c', '', '']
assert sol.shortestSubstrings(['zxy', 'yxz', 'xzy']) == ['xy', 'yx', 'zy']
assert sol.shortestSubstrings(['abc', 'def', 'abc', 'def']) == ['', '', '', '']
assert sol.shortestSubstrings(['abcdefghij' * 2, 'abcdefghij' * 2]) == ['', '']
assert sol.shortestSubstrings(['a' * 20, 'a' * 19 + 'b']) == ['aaaaaaaaaaaaaaaaaaaa', 'b']
assert sol.shortestSubstrings(['abcabcabc', 'bcabcabca', 'cabcabcab']) == ['abcabcabc', 'bcabcabca', 'cabcabcab']
