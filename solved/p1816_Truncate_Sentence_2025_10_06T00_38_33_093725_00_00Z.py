"""
URL: https://leetcode.com/problems/truncate-sentence/description/

1816. Truncate Sentence

A sentence is a list of words separated by a single space with no leading or trailing spaces. You are given a sentence s and an integer k. You want to truncate s such that it contains only the first k words. Return s after truncating it.


Example 1:

Input: s = "Hello how are you Contestant", k = 4
Output: "Hello how are you"
Explanation: The words in s are ["Hello", "how" "are", "you", "Contestant"].
The first 4 words are ["Hello", "how", "are", "you"].
Hence, you should return "Hello how are you".

Example 2:

Input: s = "What is the solution to this problem", k = 4
Output: "What is the solution"
Explanation: The words in s are ["What", "is" "the", "solution", "to", "this", "problem"].
The first 4 words are ["What", "is", "the", "solution"].
Hence, you should return "What is the solution".

Example 3:

Input: s = "chopper is not a tanuki", k = 5
Output: "chopper is not a tanuki"
Explanation: The words in s are ["chopper", "is", "not", "a", "tanuki"].
The first 5 words are ["chopper", "is", "not", "a", "tanuki"].
Hence, you should return "chopper is not a tanuki".


Constraints:

    1 <= s.length <= 500
    k is in the range [1, the number of words in s]
    s consists of only lowercase and uppercase English letters and spaces.
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
assert sol.truncateSentence("single", 1) == "single"
assert sol.truncateSentence("a b c d e", 1) == "a"
assert sol.truncateSentence("a b c d e", 5) == "a b c d e"
assert sol.truncateSentence("Mixed Case Words Here", 3) == "Mixed Case Words"
assert sol.truncateSentence("one two three", 2) == "one two"
assert sol.truncateSentence("A", 1) == "A"
assert (
    sol.truncateSentence("Long sentence with many words to test truncation", 6)
    == "Long sentence with many words to"
)
