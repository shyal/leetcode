"""
URL: https://leetcode.com/problems/most-common-word/description/

819. Most Common Word

Given a string paragraph and a string array of the banned words banned, return the most frequent word that is not banned. It is guaranteed there is at least one word that is not banned, and that the answer is unique.

The words in paragraph are case-insensitive and the answer should be returned in lowercase.

Note that words can not contain punctuation symbols.


Example 1:

Input: paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]
Output: "ball"
Explanation:
"hit" occurs 3 times, but it is a banned word.
"ball" occurs twice (and no other word does), so it is the most frequent non-banned word in the paragraph.
Note that words in the paragraph are not case sensitive,
that punctuation is ignored (even if adjacent to words, such as "ball,"),
and that "hit" isn't the answer even though it occurs more because it is banned.

Example 2:

Input: paragraph = "a.", banned = []
Output: "a"


Constraints:

        1 <= paragraph.length <= 1000
        paragraph consists of English letters, space ' ', or one of the symbols: "!?',;.".
        0 <= banned.length <= 100
        1 <= banned[i].length <= 10
        banned[i] consists of only lowercase English letters.
"""

from collections import Counter

rem = set("!?',;.")


class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        banned = set(banned)
        tmp = []
        for c in paragraph:
            if c in rem:
                tmp.append(" ")
            else:
                tmp.append(c.lower())
        count = dict(Counter("".join(tmp).split()))
        res = next(
            iter(max(count.items(), key=lambda x: x[1] if x[0] not in banned else 0)),
            "",
        )
        return res if res not in banned else ""


sol = Solution()

res = sol.mostCommonWord(paragraph="a, a, a, a, b,b,b,c, c", banned=["a"])
assert res == "b"

res = sol.mostCommonWord(
    paragraph="Bob hit a ball, the hit BALL flew far after it was hit.", banned=["hit"]
)
assert res == "ball"

res = sol.mostCommonWord(paragraph="a.", banned=[])
assert res == "a"

res = sol.mostCommonWord(paragraph="foo", banned=["foo"])
assert res == ""

res = sol.mostCommonWord(paragraph="foo foo foo", banned=["foo"])
assert res == ""

res = sol.mostCommonWord(paragraph="f f f f b b b c c", banned=["f"])
assert res == "b"
