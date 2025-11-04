"""
URL: https://leetcode.com/problems/check-if-word-equals-summation-of-two-words/description/?envType=problem-list-v2&envId=vn57k9wr

1880. Check if Word Equals Summation of Two Words

The letter value of a letter is its position in the alphabet starting from 0 (i.e. 'a' -> 0, 'b' -> 1, 'c' -> 2, etc.).

The numerical value of some string of lowercase English letters s is the concatenation of the letter values of each letter in s, which is then converted into an integer.

For example, if s = "acb", we concatenate each letter's letter value, resulting in "021". After converting it, we get 21.

You are given three strings firstWord, secondWord, and targetWord, each consisting of lowercase English letters 'a' through 'j' inclusive.

Return true if the summation of the numerical values of firstWord and secondWord equals the numerical value of targetWord, or false otherwise.

Example 1:

Input: firstWord = "acb", secondWord = "cba", targetWord = "cdb"
Output: true
Explanation:
The numerical value of firstWord is "acb" -> "021" -> 21.
The numerical value of secondWord is "cba" -> "210" -> 210.
The numerical value of targetWord is "cdb" -> "231" -> 231.
We return true because 21 + 210 == 231.

Example 2:

Input: firstWord = "aaa", secondWord = "a", targetWord = "aab"
Output: false
Explanation:
The numerical value of firstWord is "aaa" -> "000" -> 0.
The numerical value of secondWord is "a" -> "0" -> 0.
The numerical value of targetWord is "aab" -> "001" -> 1.
We return false because 0 + 0 != 1.

Example 3:

Input: firstWord = "aaa", secondWord = "a", targetWord = "aaaa"
Output: true
Explanation:
The numerical value of firstWord is "aaa" -> "000" -> 0.
The numerical value of secondWord is "a" -> "0" -> 0.
The numerical value of targetWord is "aaaa" -> "0000" -> 0.
We return true because 0 + 0 == 0.

Constraints:

    1 <= firstWord.length, secondWord.length, targetWord.length <= 8
    firstWord, secondWord, and targetWord consist of lowercase English letters from 'a' to 'j' inclusive.
"""


class Solution:
    def isSumEqual(self, firstWord: str, secondWord: str, targetWord: str) -> bool:
        to_int = lambda x: int("".join([str(ord(c) - ord("a")) for c in x]))
        return to_int(firstWord) + to_int(secondWord) == to_int(targetWord)


sol = Solution()

# print(sol.isSumEqual("acb", "cba", "cdb"))  # true

assert sol.isSumEqual("acb", "cba", "cdb") == True
assert sol.isSumEqual("aaa", "a", "aab") == False
assert sol.isSumEqual("aaa", "a", "aaaa") == True
assert sol.isSumEqual("a", "a", "a") == True
assert sol.isSumEqual("a", "a", "b") == False
assert sol.isSumEqual("j", "j", "bi") == True
assert sol.isSumEqual("j", "j", "bj") == False
assert sol.isSumEqual("jjjjjjjj", "jjjjjjjj", "jjjjjjjj") == False
assert sol.isSumEqual("jjjjjjjj", "a", "jjjjjjjj") == True
assert sol.isSumEqual("jjjjjjjj", "b", "jjjjjjjj") == False
assert sol.isSumEqual("b", "a", "ab") == True
assert sol.isSumEqual("b", "b", "ab") == False
assert sol.isSumEqual("aaa", "aaa", "aaaaaa") == True
assert sol.isSumEqual("a", "a", "aaaaaaa") == True
assert sol.isSumEqual("ijjjjjjj", "ijjjjjjj", "biiiiiii") == False
assert sol.isSumEqual("j", "a", "j") == True
assert sol.isSumEqual("aa", "aa", "aaaa") == True
# assert sol.isSumEqual("ja", "ja", "bj") == True
# assert sol.isSumEqual("ja", "ja", "bi") == False
