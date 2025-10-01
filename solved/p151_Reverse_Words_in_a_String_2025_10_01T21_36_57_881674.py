"""
151. Reverse Words in a String
Medium
Given an input string s, reverse the order of the words.

A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space.

Return a string of the words in reverse order concatenated by a single space.

Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.
 

Example 1:

Input: s = "the sky is blue"
Output: "blue is sky the"
Example 2:

Input: s = "  hello world  "
Output: "world hello"
Explanation: Your reversed string should not contain leading or trailing spaces.
Example 3:

Input: s = "a good   example"
Output: "example good a"
Explanation: You need to reduce multiple spaces between two words to a single space in the reversed string.
 

Constraints:

1 <= s.length <= 104
s contains English letters (upper-case and lower-case), digits, and spaces ' '.
There is at least one word in s.
 

Follow-up: If the string data type is mutable in your language, can you solve it in-place with O(1) extra space?
"""


class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(x for x in reversed(s.split()))


sol = Solution()

assert sol.reverseWords(s="the sky is blue") == "blue is sky the"
assert sol.reverseWords(s="  hello world  ") == "world hello"
assert sol.reverseWords(s="a good   example") == "example good a"
assert sol.reverseWords(s="hello") == "hello"
assert sol.reverseWords(s="   hello   ") == "hello"
assert sol.reverseWords(s="Python    is    great") == "great is Python"
assert sol.reverseWords(s="  OpenAI ChatGPT ") == "ChatGPT OpenAI"
assert sol.reverseWords(s="123 456 789") == "789 456 123"
assert sol.reverseWords(s="abc123 def456") == "def456 abc123"
assert (
    sol.reverseWords(s="one two three four five six seven eight nine ten")
    == "ten nine eight seven six five four three two one"
)
assert sol.reverseWords(s="a") == "a"
assert sol.reverseWords(s="word1                    word2") == "word2 word1"

