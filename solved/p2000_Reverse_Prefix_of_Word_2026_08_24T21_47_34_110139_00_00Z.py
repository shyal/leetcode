"""
URL: https://leetcode.com/problems/reverse-prefix-of-word/description/?envType=problem-list-v2&envId=vn57k9wr

2000. Reverse Prefix of Word

Given a 0-indexed string word and a character ch, reverse the segment of word that starts at index 0 and ends at the index of the first occurrence of ch (inclusive). If the character ch does not exist in word, do nothing.

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
            return word[: index + 1][::-1] + word[index + 1 :]
        return word


sol = Solution()

print(sol.reversePrefix("abcdefd", "d"))  # "dcbaefd"

assert sol.reversePrefix("abcdefd", "d") == "dcbaefd"
assert sol.reversePrefix("xyxzxe", "z") == "zxyxxe"
assert sol.reversePrefix("abcd", "z") == "abcd"

assert sol.reversePrefix("", "a") == ""
assert sol.reversePrefix("a", "a") == "a"
assert sol.reversePrefix("a", "b") == "a"
assert sol.reversePrefix("aaaaa", "a") == "aaaaa"
assert sol.reversePrefix("abcde", "e") == "edcba"
assert sol.reversePrefix("abcde", "a") == "abcde"
assert sol.reversePrefix("abcde", "c") == "cbade"
assert sol.reversePrefix("abcde", "z") == "abcde"
