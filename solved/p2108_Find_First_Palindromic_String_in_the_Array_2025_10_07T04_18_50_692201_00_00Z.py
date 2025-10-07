"""
URL: https://leetcode.com/problems/find-first-palindromic-string-in-the-array/description/

2108. Find First Palindromic String in the Array

Given an array of strings words, return the first palindromic string in the array. If there is no such string, return an empty string "".

A string is palindromic if it reads the same forward and backward.

Example 1:

Input: words = ["abc","car","ada","racecar","cool"]
Output: "ada"
Explanation: "ada" is the first string that is a palindrome.
"racecar" is also a palindrome, but it is not the first.

Example 2:

Input: words = ["notapalindrome","racecar"]
Output: "racecar"
Explanation: The first and only string that is a palindrome is "racecar".

Example 3:

Input: words = ["def","ghi"]
Output: ""
Explanation: There are no palindromic strings so we return an empty string.

Constraints:

    1 <= words.length <= 100
    1 <= words[i].length <= 100
    words[i] consists only of lowercase English letters.
"""


class Solution:
    def firstPalindrome(self, words: List[str]) -> str:
        return next((x for x in words if x == x[::-1]), "")


sol = Solution()

# print(sol.firstPalindrome(["abc", "car", "ada", "racecar", "cool"]))  # "ada"

assert sol.firstPalindrome(["abc", "car", "ada", "racecar", "cool"]) == "ada"
assert sol.firstPalindrome(["notapalindrome", "racecar"]) == "racecar"
assert sol.firstPalindrome(["def", "ghi"]) == ""
assert sol.firstPalindrome(["a"]) == "a"
assert sol.firstPalindrome(["ab"]) == ""
assert sol.firstPalindrome(["aa", "ab"]) == "aa"
assert sol.firstPalindrome(["ab", "aa"]) == "aa"
assert sol.firstPalindrome(["abba", "abc"]) == "abba"
assert sol.firstPalindrome(["abcba", "defed"]) == "abcba"
assert sol.firstPalindrome(["a", "b", "c"]) == "a"
assert sol.firstPalindrome(["abc", "def", "ghi"]) == ""
assert sol.firstPalindrome(["racecar"]) == "racecar"
assert sol.firstPalindrome(["not", "a", "palindrome"]) == "a"
assert sol.firstPalindrome(["level", "noon", "radar"]) == "level"
assert sol.firstPalindrome(["xyz", "zyx"]) == ""
