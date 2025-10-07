"""
URL: https://leetcode.com/problems/unique-morse-code-words/description/

804. Unique Morse Code Words

International Morse Code defines a standard encoding where each letter is mapped to a series of dots and dashes, as follows:

    'a' maps to ".-",
    'b' maps to "-...",
    'c' maps to "-.-.", and so on.

For convenience, the full table for the 26 letters of the English alphabet is given below:

[".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]

Given an array of strings words where each word can be written as a concatenation of the Morse code of each letter.

    For example, "cab" can be written as "-.-..--...", which is the concatenation of "-.-.", ".-", and "-...". We will call such a concatenation the transformation of a word.

Return the number of different transformations among all words we have.

Example 1:

Input: words = ["gin","zen","gig","msg"]
Output: 2
Explanation: The transformation of each word is:
"gin" -> "--...-."
"zen" -> "--...-."
"gig" -> "--...--."
"msg" -> "--...--."
There are 2 different transformations: "--...-." and "--...--.".

Example 2:

Input: words = ["a"]
Output: 1

Constraints:

    1 <= words.length <= 100
    1 <= words[i].length <= 12
    words[i] consists of lowercase English letters.
"""


class Solution:
    def uniqueMorseRepresentations(self, words: List[str]) -> int:
        morse = [
            ".-",
            "-...",
            "-.-.",
            "-..",
            ".",
            "..-.",
            "--.",
            "....",
            "..",
            ".---",
            "-.-",
            ".-..",
            "--",
            "-.",
            "---",
            ".--.",
            "--.-",
            ".-.",
            "...",
            "-",
            "..-",
            "...-",
            ".--",
            "-..-",
            "-.--",
            "--..",
        ]
        code = {l: morse[i] for i, l in enumerate(ascii_lowercase)}
        return len(set([("".join(code[c] for c in word)) for word in words]))


sol = Solution()

# print(sol.uniqueMorseRepresentations(["gin", "zen", "gig", "msg"]))  # 2

assert sol.uniqueMorseRepresentations(["gin", "zen", "gig", "msg"]) == 2
assert sol.uniqueMorseRepresentations(["a"]) == 1
assert sol.uniqueMorseRepresentations(["gin", "zen"]) == 1
assert sol.uniqueMorseRepresentations(["gin", "gig"]) == 2
assert sol.uniqueMorseRepresentations([]) == 0
assert sol.uniqueMorseRepresentations(["a" * 12]) == 1
assert sol.uniqueMorseRepresentations(["a", "b", "c", "d", "e"]) == 5
