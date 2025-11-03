"""
URL: https://leetcode.com/problems/maximum-value-of-a-string-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

2496. Maximum Value of a String in an Array

The value of an alphanumeric string can be defined as:

- The numeric representation of the string in base 10, if it comprises of digits only.
- The length of the string, otherwise.

Given an array strs of alphanumeric strings, return the maximum value of any string in strs.


Example 1:

Input: strs = ["alic3","bob","3","4","00000"]
Output: 5
Explanation:
- "alic3" consists of both letters and digits, so its value is its length, i.e. 5.
- "bob" consists only of letters, so its value is also its length, i.e. 3.
- "3" consists only of digits, so its value is its numeric equivalent, i.e. 3.
- "4" also consists only of digits, so its value is 4.
- "00000" consists only of digits, so its value is 0.
Hence, the maximum value is 5, of "alic3".

Example 2:

Input: strs = ["1","01","001","0001"]
Output: 1
Explanation:
Each string in the array has value 1. Hence, we return 1.


Constraints:

- 1 <= strs.length <= 100
- 1 <= strs[i].length <= 9
- strs[i] consists of only lowercase English letters and digits.
"""


class Solution:
    def maximumValue(self, strs: List[str]) -> int:
        is_digits = lambda s: all("0" <= x <= "9" for x in s)
        val = lambda s: int(s) if is_digits(s) else len(s)
        return max(val(x) for x in strs)


sol = Solution()

# print(sol.maximumValue(["alic3", "bob", "3", "4", "00000"]))  # 5

assert sol.maximumValue(["alic3", "bob", "3", "4", "00000"]) == 5
assert sol.maximumValue(["1", "01", "001", "0001"]) == 1
assert sol.maximumValue(["a"]) == 1
assert sol.maximumValue(["0"]) == 0
assert sol.maximumValue(["999999999"]) == 999999999
assert sol.maximumValue(["aaaaaaaaa"]) == 9
assert sol.maximumValue(["000000000", "a"]) == 1
assert sol.maximumValue(["10", "a"]) == 10
assert sol.maximumValue(["a1b2c3d4e"]) == 9
assert sol.maximumValue(["123456789"]) == 123456789
assert sol.maximumValue(["00100"]) == 100
assert sol.maximumValue(["100a"]) == 4
assert sol.maximumValue(["0", "1", "a"]) == 1
assert sol.maximumValue(["abc", "defg", "hijklmno"]) == 8
assert sol.maximumValue(["9", "99", "999"]) == 999
