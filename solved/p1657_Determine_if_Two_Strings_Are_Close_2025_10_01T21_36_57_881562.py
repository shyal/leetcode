"""
1657. Determine if Two Strings Are Close
Medium
Two strings are considered close if you can attain one from the other using the following operations:

Operation 1: Swap any two existing characters.
For example, abcde -> aecdb
Operation 2: Transform every occurrence of one existing character into another existing character, and do the same with the other character.
For example, aacabb -> bbcbaa (all a's turn into b's, and all b's turn into a's)
You can use the operations on either string as many times as necessary.

Given two strings, word1 and word2, return true if word1 and word2 are close, and false otherwise.

Example 1:

Input: word1 = "abc", word2 = "bca"
Output: true
Explanation: You can attain word2 from word1 in 2 operations.
Apply Operation 1: "abc" -> "acb"
Apply Operation 1: "acb" -> "bca"
Example 2:

Input: word1 = "a", word2 = "aa"
Output: false
Explanation: It is impossible to attain word2 from word1, or vice versa, in any number of operations.
Example 3:

Input: word1 = "cabbba", word2 = "abbccc"
Output: true
Explanation: You can attain word2 from word1 in 3 operations.
Apply Operation 1: "cabbba" -> "caabbb"
Apply Operation 2: "caabbb" -> "baaccc"
Apply Operation 2: "baaccc" -> "abbccc"
 

Constraints:

1 <= word1.length, word2.length <= 105
word1 and word2 contain only lowercase English letters.
"""

from collections import Counter


class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False
        c1, c2 = dict(Counter(word1)), dict(Counter(word2))
        letters_match = [*sorted(c1.keys())] == [*sorted(c2.keys())]
        counts_match = [*sorted(c1.values())] == [*sorted(c2.values())]
        return letters_match and counts_match


sol = Solution()
assert sol.closeStrings(word1="abc", word2="bca") == True
assert sol.closeStrings(word1="a", word2="aa") == False
assert sol.closeStrings(word1="cabbba", word2="abbccc") == True
assert sol.closeStrings(word1="a", word2="a") == True
assert sol.closeStrings(word1="a", word2="b") == False
assert sol.closeStrings(word1="ab", word2="ba") == True
assert sol.closeStrings(word1="ab", word2="aa") == False
assert sol.closeStrings(word1="aaabbc", word2="ccbbba") == True
assert sol.closeStrings(word1="aaabbc", word2="aabbcc") == False
assert sol.closeStrings(word1="abcd", word2="dcba") == True
assert sol.closeStrings(word1="aaaa", word2="bbbb") == False
assert sol.closeStrings(word1="abc", word2="abcd") == False
assert sol.closeStrings(word1="aabbccddeeff", word2="abcdeffedcba") == True
assert sol.closeStrings(word1="abb", word2="baa") == True
assert sol.closeStrings(word1="aaabbbccc", word2="aabbccdde") == False

