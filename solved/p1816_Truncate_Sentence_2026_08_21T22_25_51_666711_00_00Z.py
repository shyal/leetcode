"""
URL: https://leetcode.com/problems/truncate-sentence/description/?envType=problem-list-v2&envId=vn57k9wr

1816. Truncate Sentence

A sentence is a list of words that are separated by a single space with no leading or trailing spaces. Each of the words consists of only uppercase and lowercase English letters (no punctuation).

For example, "Hello World", "HELLO", and "hello world hello world" are all sentences.

You are given a sentence s and an integer k. You want to truncate s such that it contains only the first k words. Return s after truncating it.

Example 1:

Input: s = "Hello how are you Contestant", k = 4
Output: "Hello how are you"
Explanation:
The words in s are ["Hello", "how", "are", "you", "Contestant"].
The first 4 words are ["Hello", "how", "are", "you"].
Hence, you should return "Hello how are you".

Example 2:

Input: s = "What is the solution to this problem", k = 4
Output: "What is the solution"
Explanation:
The words in s are ["What", "is", "the", "solution", "to", "this", "problem"].
The first 4 words are ["What", "is", "the", "solution"].
Hence, you should return "What is the solution".

Example 3:

Input: s = "chopper is not a tanuki", k = 5
Output: "chopper is not a tanuki"

Constraints:

    1 <= s.length <= 500
    k is in the range [1, the number of words in s].
    s consist of only lowercase and uppercase English letters and spaces.
    The words in s are separated by a single space.
    There are no leading or trailing spaces.
"""


class Solution:
    def truncateSentence(self, s: str, k: int) -> str:
        return " ".join(s.split()[:k])


sol = Solution()

print(sol.truncateSentence("Hello how are you Contestant", 4))  # "Hello how are you"

assert sol.truncateSentence("Hello how are you Contestant", 4) == "Hello how are you"
assert (
    sol.truncateSentence("What is the solution to this problem", 4)
    == "What is the solution"
)
assert sol.truncateSentence("chopper is not a tanuki", 5) == "chopper is not a tanuki"

assert sol.truncateSentence("word", 1) == "word"
assert sol.truncateSentence("repeat repeat repeat repeat", 2) == "repeat repeat"
assert sol.truncateSentence("a b c d e f g h i j", 10) == "a b c d e f g h i j"
assert sol.truncateSentence("a b c d e f g h i j", 1) == "a"
assert sol.truncateSentence("Hello", 1) == "Hello"
assert sol.truncateSentence("Hello world", 1) == "Hello"
assert sol.truncateSentence("Hello world", 2) == "Hello world"
assert (
    sol.truncateSentence("a" * 500, 1)
    == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)
assert (
    sol.truncateSentence("a b c d e f g h i j k l m n o p q r s t u v w x y z", 26)
    == "a b c d e f g h i j k l m n o p q r s t u v w x y z"
)
assert (
    sol.truncateSentence("one two three four five six seven eight nine ten", 5)
    == "one two three four five"
)
assert sol.truncateSentence("UPPER lower MIXED Case", 3) == "UPPER lower MIXED"
assert sol.truncateSentence("a a a a a a a a a a", 5) == "a a a a a"
