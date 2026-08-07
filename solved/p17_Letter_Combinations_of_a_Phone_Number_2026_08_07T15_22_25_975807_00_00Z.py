"""
URL: https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/?envType=problem-list-v2&envId=vn57k9wr

17. Letter Combinations of a Phone Number

Given a string containing digits from 2-9 inclusive, return all possible
letter combinations that the number could represent. Return the answer in
any order.

A mapping of digits to letters (just like on the telephone buttons) is
given below. Note that 1 does not map to any letters.

    2 -> abc
    3 -> def
    4 -> ghi
    5 -> jkl
    6 -> mno
    7 -> pqrs
    8 -> tuv
    9 -> wxyz


Example 1:

Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:

Input: digits = "2"
Output: ["a","b","c"]


Constraints:

    1 <= digits.length <= 4
    digits[i] is a digit in the range ['2', '9'].
"""

D = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        ret = []

        def DP(i):
            if len(ret) == len(digits):
                res.append(''.join(ret[:]))
                return
            for j in range(0, len(D[digits[i]])):
                ret.append(D[digits[i]][j])
                DP(i+1)
                ret.pop()
        if digits:
            DP(0)
        return res


sol = Solution()

# print(sol.letterCombinations("23"))  # ["ad","ae","af","bd","be","bf","cd","ce","cf"]

assert sorted(sol.letterCombinations("23")) == sorted(
    ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
)
assert sorted(sol.letterCombinations("2")) == sorted(["a", "b", "c"])

assert sol.letterCombinations("") == []

assert sorted(sol.letterCombinations("7")) == sorted(["p", "q", "r", "s"])
assert sorted(sol.letterCombinations("9")) == sorted(["w", "x", "y", "z"])
assert sorted(sol.letterCombinations("8")) == sorted(["t", "u", "v"])

assert sorted(sol.letterCombinations("22")) == sorted(
    ["aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"]
)

assert sorted(sol.letterCombinations("79")) == sorted(
    [
        "pw", "px", "py", "pz",
        "qw", "qx", "qy", "qz",
        "rw", "rx", "ry", "rz",
        "sw", "sx", "sy", "sz",
    ]
)

result_234 = sol.letterCombinations("234")
assert len(result_234) == 27
assert len(set(result_234)) == 27
assert "adg" in result_234
assert "cfi" in result_234
assert all(len(combo) == 3 for combo in result_234)

result_7777 = sol.letterCombinations("7777")
assert len(result_7777) == 256
assert len(set(result_7777)) == 256
assert "pppp" in result_7777
assert "ssss" in result_7777
assert all(len(combo) == 4 for combo in result_7777)
assert all(set(combo) <= set("pqrs") for combo in result_7777)

result_2345 = sol.letterCombinations("2345")
assert len(result_2345) == 81
assert len(set(result_2345)) == 81
assert "adgj" in result_2345
assert "cfil" in result_2345
assert all(len(combo) == 4 for combo in result_2345)

assert sol.letterCombinations("23")[0] == "ad"
assert sol.letterCombinations("23")[-1] == "cf"

print("All asserts passed")