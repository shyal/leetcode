"""
EPI 16.11 The pretty printing problem

Given a list words and line_length, split words, in order, into lines.
The words of a line are joined by single spaces, and a line holds at
most line_length characters. The messiness of a line of c characters is
(line_length - c)^2, and the messiness of a split is the sum over all
its lines, the last line too. Return the least messiness of a split.

Example 1:

Input: words = ["aaa", "bb", "cc", "ddddd"], line_length = 6
Output: 11
Explanation: the split

    aaa      3 characters, messiness 9
    bb cc    5 characters, messiness 1
    ddddd    5 characters, messiness 1

Putting as many words as fit on each line gives "aaa bb", "cc",
"ddddd" and a messiness of 0 + 16 + 1 = 17.

Example 2:

Input: words = ["abc"], line_length = 5
Output: 4

Example 3:

Input: words = ["a", "b", "c"], line_length = 5
Output: 0
Explanation: "a b c" has 5 characters.

Constraints:

    1 <= len(words) <= 500
    1 <= len(words[i]) <= line_length <= 100

    REQUIRED: O(len(words) * line_length) time. NO enumeration of every
    split.
"""


class Solution:
    def minimum_messiness(self, words: list[str], line_length: int) -> int:
        pass


sol = Solution()

print(sol.minimum_messiness(["aaa", "bb", "cc", "ddddd"], 6))  # 11

# assert sol.minimum_messiness(["aaa", "bb", "cc", "ddddd"], 6) == 11
# assert sol.minimum_messiness(["abc"], 5) == 4
# assert sol.minimum_messiness(["a", "b", "c"], 5) == 0
# assert sol.minimum_messiness(["abc"], 3) == 0
# assert sol.minimum_messiness(["a", "b", "c"], 1) == 0
# assert sol.minimum_messiness(["aaaa", "bb", "cc"], 7) == 13
# assert sol.minimum_messiness(["a", "bb", "ccc", "dddd"], 4) == 1
# assert sol.minimum_messiness(["ab", "cd", "ef", "gh"], 5) == 0
# assert sol.minimum_messiness(["a"] * 7, 3) == 4
# assert sol.minimum_messiness(["xy"] * 300, 8) == 0
# assert sol.minimum_messiness(["x" * (i % 5 + 1) for i in range(500)], 20) == 100
# assert sol.minimum_messiness([chr(97 + i % 26) * (i * 7 % 9 + 1) for i in range(400)], 30) == 1466
