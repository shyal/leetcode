"""
URL: https://leetcode.com/problems/valid-palindrome/description/?envType=problem-list-v2&envId=vn57k9wr

125. Valid Palindrome

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:

    1 <= s.length <= 2 * 10^5
    s consists only of printable ASCII characters.
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = ''.join([_.lower() for _ in s if _.isalnum()])
        return s == s[::-1]



sol = Solution()

# print(sol.isPalindrome("A man, a plan, a canal: Panama"))  # true

assert sol.isPalindrome("A man, a plan, a canal: Panama") == True
assert sol.isPalindrome("race a car") == False
assert sol.isPalindrome(" ") == True
assert sol.isPalindrome("") == True
assert sol.isPalindrome("a") == True
assert sol.isPalindrome("aa") == True
assert sol.isPalindrome("ab") == False
assert sol.isPalindrome("a.") == True
assert sol.isPalindrome(".,") == True
assert sol.isPalindrome("0P") == False
assert sol.isPalindrome("1a2") == False
assert sol.isPalindrome("121") == True
assert sol.isPalindrome("12 21") == True
assert sol.isPalindrome("Ab Ba") == True
assert sol.isPalindrome("No 'x' in Nixon") == True
assert sol.isPalindrome("ab2a") == False
assert sol.isPalindrome("ab!!ba") == True
assert sol.isPalindrome("ab!!ca") == False
assert sol.isPalindrome(".,a,.") == True
assert sol.isPalindrome("a.,b,.,a") == True
assert sol.isPalindrome("A1b2c2b1a") == True
assert sol.isPalindrome("A1b2c3b1a") == False
assert sol.isPalindrome("12321") == True
assert sol.isPalindrome("12345") == False
assert sol.isPalindrome("!@#$%") == True
assert sol.isPalindrome("a!b!c!b!a") == True
assert sol.isPalindrome("a!b!c!d!a") == False