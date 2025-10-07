"""
URL: https://leetcode.com/problems/check-if-the-sentence-is-pangram/description/

1832. Check if the Sentence Is Pangram

A pangram is a sentence where every letter of the English alphabet appears at least once.

Given a string sentence containing only lowercase English letters, return true if sentence is a pangram, or false otherwise.


Example 1:

Input: sentence = "thequickbrownfoxjumpsoverthelazydog"
Output: true
Explanation: sentence contains at least one of every letter of the English alphabet.

Example 2:

Input: sentence = "leetcode"
Output: false


Constraints:

    1 <= sentence.length <= 1000
    sentence consists of lowercase English letters.
"""


class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        counter = Counter(sentence)
        return all(counter.get(c, 0) >= 1 for c in ascii_lowercase)


sol = Solution()

# print(sol.checkIfPangram("thequickbrownfoxjumpsoverthelazydog"))  # true

assert sol.checkIfPangram("thequickbrownfoxjumpsoverthelazydog") == True
assert sol.checkIfPangram("leetcode") == False
assert sol.checkIfPangram("a") == False
assert sol.checkIfPangram("abcdefghijklmnopqrstuvwxyz") == True
assert sol.checkIfPangram("abcdefghijklmnopqrstuvwxy") == False
assert (
    sol.checkIfPangram(
        "aaaaabbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwxxxxxyyyyyzzzzz"
    )
    == True
)
assert (
    sol.checkIfPangram(
        "aaaaabbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwxxxxxyyyyy"
    )
    == False
)
# assert sol.checkIfPangram("abcdeffghijklmmnopqrstuuvwxyz") == False
assert sol.checkIfPangram("a" * 1000) == False
assert sol.checkIfPangram("thequickbrownfoxjumpsoverthelazydog" * 10) == True
