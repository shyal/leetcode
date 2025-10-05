"""
URL: https://leetcode.com/problems/reverse-prefix-of-word/description/?envType=study-plan-v2&envId=leetcode-75

2000. Reverse Prefix of Word

Given a 0-indexed string word and a character ch, reverse the segment of word that starts at index 0 and ends at the index of the first occurrence of ch (inclusive). If the character ch does not appear in word, do nothing.

For example, if word = "abcdefd" and ch = "d", then you should reverse the segment that starts at 0 and ends at 3 (inclusive). The resulting string will be "dcbaefd".

Return the resulting string.


Example 1:

Input: word = "abcdefd", ch = "d"
Output: "dcbaefd"
Explanation: The first occurrence of "d" is at index 3.
Reverse the part of word from 0 to 3 (inclusive), the resulting string is "dcbaefd".

Example 2:

Input: word = "xyxzxe", ch = "z"
Output: "zxyxxe"
Explanation: The first and only occurrence of "z" is at index 3.
Reverse the part of word from 0 to 3 (inclusive), the resulting string is "zxyxxe".

Example 3:

Input: word = "abcd", ch = "z"
Output: "abcd"
Explanation: "z" does not exist in word.
You should not do any reverse operation, the resulting string is "abcd".


Constraints:

    1 <= word.length <= 250
    word consists of lowercase English letters.
    ch is a lowercase English letter.

"""


class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        if ch in word:
            index = word.index(ch)
            a = word[: index + 1][::-1]
            b = word[index + 1 :]
            return a + b
        return word


sol = Solution()

assert sol.reversePrefix("abcdefd", "d") == "dcbaefd"
assert sol.reversePrefix("xyxzxe", "z") == "zxyxxe"
assert sol.reversePrefix("abcd", "z") == "abcd"
assert sol.reversePrefix("a", "a") == "a"
assert sol.reversePrefix("a", "b") == "a"
assert sol.reversePrefix("aa", "a") == "aa"
assert sol.reversePrefix("abc", "c") == "cba"
assert sol.reversePrefix("abcd", "d") == "dcba"
assert sol.reversePrefix("abcdc", "c") == "cbadc"
assert sol.reversePrefix("zabc", "z") == "zabc"
assert sol.reversePrefix("aaaaa", "a") == "aaaaa"
assert sol.reversePrefix("abcde", "e") == "edcba"
assert sol.reversePrefix("abcde", "f") == "abcde"
assert sol.reversePrefix("xyz", "x") == "xyz"
assert sol.reversePrefix("xyz", "y") == "yxz"
assert sol.reversePrefix("xyz", "z") == "zyx"
