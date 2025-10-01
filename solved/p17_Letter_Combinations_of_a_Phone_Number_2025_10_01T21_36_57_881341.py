"""
URL: https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/?envType=study-plan-v2&envId=leetcode-75

17. Letter Combinations of a Phone Number

Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.


Example 1:

Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:

Input: digits = ""
Output: []

Example 3:

Input: digits = "2"
Output: ["a","b","c"]


Constraints:

        0 <= digits.length <= 4
        digits[i] is a digit in the range ['2', '9'].
"""

from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        letters = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
        digits = [int(x) for x in digits]
        letters = [letters[i] for i in digits]

        def dfs(depth=0, path=""):
            if depth == len(digits):
                combos.append(path)
                return
            for i, l in enumerate(letters[depth]):
                dfs(depth + 1, path + l)

        combos = []
        dfs()
        return combos


sol = Solution()

res = sol.letterCombinations(digits="22")
assert res == ["aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"]

res = sol.letterCombinations(digits="23")
assert res == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]

res = sol.letterCombinations(digits="2")
assert res == ["a", "b", "c"]

res = sol.letterCombinations(digits="27")
assert res == ["ap", "aq", "ar", "as", "bp", "bq", "br", "bs", "cp", "cq", "cr", "cs"]

res = sol.letterCombinations(digits="468")
assert res == [
    "gmt",
    "gmu",
    "gmv",
    "gnt",
    "gnu",
    "gnv",
    "got",
    "gou",
    "gov",
    "hmt",
    "hmu",
    "hmv",
    "hnt",
    "hnu",
    "hnv",
    "hot",
    "hou",
    "hov",
    "imt",
    "imu",
    "imv",
    "int",
    "inu",
    "inv",
    "iot",
    "iou",
    "iov",
]
