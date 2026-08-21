"""
URL: https://leetcode.com/problems/maximum-number-of-words-found-in-sentences/description/?envType=problem-list-v2&envId=vn57k9wr

2114. Maximum Number of Words Found in Sentences

A sentence is a list of words that are separated by a single space with no leading or trailing spaces.

You are given an array of strings sentences, where each sentences[i] represents a single sentence.

Return the maximum number of words that appear in a single sentence.

Example 1:

Input: sentences = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]
Output: 6
Explanation:
- The first sentence, "alice and bob love leetcode", has 5 words in total.
- The second sentence, "i think so too", has 4 words in total.
- The third sentence, "this is great thanks very much", has 6 words in total.
Thus, the maximum number of words in a single sentence comes from the third sentence, which has 6 words.

Example 2:

Input: sentences = ["please wait", "continue to fight", "continue to win"]
Output: 3
Explanation: It is possible that multiple sentences contain the same number of words.
In this example, the second and third sentences have the same number of words.

Constraints:

    1 <= sentences.length <= 100
    1 <= sentences[i].length <= 100
    sentences[i] consists only of lowercase English letters and ' ' only.
    sentences[i] does not have leading or trailing spaces.
    All the words in sentences[i] are separated by a single space.
"""


class Solution:
    def mostWordsFound(self, sentences: List[str]) -> int:
        return max(len(s.split()) for s in sentences)


sol = Solution()

print(
    sol.mostWordsFound(
        [
            "alice and bob love leetcode",
            "i think so too",
            "this is great thanks very much",
        ]
    )
)  # 6

assert (
    sol.mostWordsFound(
        [
            "alice and bob love leetcode",
            "i think so too",
            "this is great thanks very much",
        ]
    )
    == 6
)
assert sol.mostWordsFound(["please wait", "continue to fight", "continue to win"]) == 3

assert sol.mostWordsFound(["word"]) == 1
assert sol.mostWordsFound(["a b c d e f g h i j k l m n o p q r s t u v w x y z"]) == 26
assert sol.mostWordsFound(["one", "two two", "three three three"]) == 3
assert sol.mostWordsFound(["-1 -2 -3", "-4 -5", "-6"]) == 3
assert sol.mostWordsFound(["a " * 99 + "a"]) == 100
assert sol.mostWordsFound(["a"] * 100) == 1
assert sol.mostWordsFound(["a b c"] * 100) == 3
assert sol.mostWordsFound([""] * 1) == 0
assert sol.mostWordsFound(["a " * 49 + "a", "b " * 50 + "b"]) == 51
assert (
    sol.mostWordsFound(
        ["repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat"]
    )
    == 10
)
assert sol.mostWordsFound(["single"]) == 1
assert (
    sol.mostWordsFound(["a b c d e f g h i j k l m n o p q r s t u v w x y z"] * 100)
    == 26
)
