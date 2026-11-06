"""
A word of lowercase letters is encrypted in three steps. Step 1:
replace each letter by its ASCII value. Step 2: add 1 to the first
value, then add to every later value the step 2 value of the letter
before it. Step 3: subtract 26 from each value until it is in the range
97 to 122, the ASCII values of 'a' to 'z', and turn the values back
into letters. For the word "crime":

    letter    c     r     i     m     e
    step 1    99    114   105   109   101
    step 2    100   214   319   428   529
    step 3    100   110   111   116   113
    letter    d     n     o     t     q

Given the encrypted string word, return the word it was made from.

Example 1:

Input: word = "dnotq"
Output: "crime"

Example 2:

Input: word = "rajsb"
Output: "qqqqq"
Explanation: step 2 of "qqqqq" is 114, 227, 340, 453, 566.

Example 3:

Input: word = ""
Output: ""

Constraints:

    0 <= len(word) <= 10^5
    word consists of lowercase English letters.

    REQUIRED: O(n) time. NO loop that adds or subtracts 26 more than
    once per letter.
"""


class Solution:
    def decrypt(self, word: str) -> str:
        pass


sol = Solution()

print(sol.decrypt("dnotq"))  # crime

# assert sol.decrypt("dnotq") == "crime"
# assert sol.decrypt("rajsb") == "qqqqq"
# assert sol.decrypt("") == ""
# assert sol.decrypt("flgxswdliefy") == "encyclopedia"
# assert sol.decrypt("bvqmjhgghjmqvbiqzjugthwmdv") == "abcdefghijklmnopqrstuvwxyz"
# assert sol.decrypt("eobamwpnlmhklrq") == "drugtrafficking"
# assert sol.decrypt("b") == "a"
# assert sol.decrypt("a") == "z"
# assert sol.decrypt("bu") == "aa"
# assert sol.decrypt("bungzslexqjcvohatmfyrkdwpi" * 3846) == "a" * 99996
