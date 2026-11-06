"""
Given two lists of words sentence1 and sentence2 and a list similarPairs
of word pairs, return True when the two sentences are similar, else
False. The sentences are similar when they have the same length and the
words at each index are similar. Two words are similar when they are
equal, when they form a pair in similarPairs, or when each of them is
similar to a third word.

Example 1:

Input: sentence1 = ["I", "really", "love", "leetcode", "and", "apples"],
       sentence2 = ["I", "so", "like", "codesignal", "and", "oranges"],
       similarPairs = [["very", "so"], ["love", "adore"], ["really", "very"],
                       ["leetcode", "codesignal"], ["apples", "oranges"],
                       ["like", "adore"]]
Output: True
Explanation: "love" and "like" are not a pair, but both are paired with
"adore". "really" and "so" are joined through "very".

Example 2:

Input: sentence1 = ["I", "love", "to", "play", "football"],
       sentence2 = ["I", "love", "playing", "soccer"],
       similarPairs = [["play", "playing"], ["football", "soccer"]]
Output: False
Explanation: the lengths differ.

Example 3:

Input: sentence1 = ["Do", "you", "like", "coffee"],
       sentence2 = ["Do", "you", "love", "coffee"],
       similarPairs = [["like", "enjoy"], ["coffee", "tea"]]
Output: False
Explanation: no chain of pairs joins "like" to "love".

Constraints:

    0 <= len(sentence1), len(sentence2) <= 1000
    0 <= len(similarPairs) <= 2000
    1 <= len(word) <= 20, words are case sensitive

    REQUIRED: O(n + m) time for n words and m pairs, after near-constant
    union-find operations. NO DFS or BFS per index. Use union-find.
"""


class Solution:
    def areSentencesSimilar(self, sentence1: list[str], sentence2: list[str], similarPairs: list[list[str]]) -> bool:
        pass


sol = Solution()

print(
    sol.areSentencesSimilar(
        ["I", "really", "love", "leetcode", "and", "apples"],
        ["I", "so", "like", "codesignal", "and", "oranges"],
        [["very", "so"], ["love", "adore"], ["really", "very"], ["leetcode", "codesignal"], ["apples", "oranges"], ["like", "adore"]],
    )
)  # True

# assert sol.areSentencesSimilar(["I", "really", "love", "leetcode", "and", "apples"], ["I", "so", "like", "codesignal", "and", "oranges"], [["very", "so"], ["love", "adore"], ["really", "very"], ["leetcode", "codesignal"], ["apples", "oranges"], ["like", "adore"]]) is True
# assert sol.areSentencesSimilar(["I", "love", "to", "play", "football"], ["I", "love", "playing", "soccer"], [["play", "playing"], ["football", "soccer"]]) is False
# assert sol.areSentencesSimilar(["Do", "you", "like", "coffee"], ["Do", "you", "love", "coffee"], [["like", "enjoy"], ["coffee", "tea"]]) is False
# assert sol.areSentencesSimilar(["Let's", "code", "in", "Python"], ["Let's", "program", "in", "Python"], [["code", "program"]]) is True
# assert sol.areSentencesSimilar(["i", "love", "coding"], ["i", "love", "coding"], []) is True
# assert sol.areSentencesSimilar(["i", "love", "coding"], ["i", "really", "love", "coding"], []) is False
# assert sol.areSentencesSimilar(["i", "love", "coding"], ["i", "adore", "coding"], [["love", "adore"]]) is True
# assert sol.areSentencesSimilar(["i", "enjoy", "coding", "very", "much"], ["i", "love", "programming", "so", "much"], [["enjoy", "love"], ["coding", "programming"], ["very", "so"]]) is True
# assert sol.areSentencesSimilar(["i", "enjoy", "coding", "very", "much"], ["i", "love", "programming", "so", "much"], [["enjoy", "love"], ["very", "so"]]) is False
# assert sol.areSentencesSimilar([], [], []) is True
# assert sol.areSentencesSimilar([], ["a"], []) is False
# assert sol.areSentencesSimilar(["a"], ["b"], [["b", "a"]]) is True
# assert sol.areSentencesSimilar(["a"], ["d"], [["a", "b"], ["b", "c"], ["c", "d"]]) is True
# assert sol.areSentencesSimilar(["a"], ["d"], [["a", "b"], ["c", "d"]]) is False
# assert sol.areSentencesSimilar(["A"], ["a"], []) is False
# assert sol.areSentencesSimilar(["w0"], ["w2000"], [["w" + str(i), "w" + str(i + 1)] for i in range(2000)]) is True
# assert sol.areSentencesSimilar(["w" + str(i) for i in range(1000)], ["w" + str(1999 - i) for i in range(1000)], [["w" + str(i), "w" + str(i + 1)] for i in range(2000)]) is True
# assert sol.areSentencesSimilar(["w" + str(i) for i in range(1000)], ["w" + str(1999 - i) for i in range(1000)], [["w" + str(i), "w" + str(i + 1)] for i in range(999)]) is False
