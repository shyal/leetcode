"""
URL: https://leetcode.com/problems/finding-3-digit-even-numbers/description/?envType=problem-list-v2&envId=vn57k9wr

2094. Finding 3-Digit Even Numbers

You are given an integer array digits, where each element is a digit. The array may contain duplicates.

You need to find all the unique integers that follow the given requirements:

        The integer consists of the concatenation of three elements from digits in any arbitrary order.
        The integer does not have leading zeros.
        The integer is even.

For example, if the given digits were [1, 2, 3], integers 132 and 312 follow the requirements.

Return a sorted array of the unique integers.


Example 1:

Input: digits = [2,1,3,0]
Output: [102,120,130,132,210,230,302,310,312,320]
Explanation: All the possible integers that follow the requirements are in the output array.
Notice that there are no odd integers or integers with leading zeros.

Example 2:

Input: digits = [2,2,8,8,2]
Output: [222,228,282,288,822,828,882]
Explanation: The same digit can be used as many times as it appears in digits.
In this example, the digit 8 is used twice each time in 288, 828, and 882.

Example 3:

Input: digits = [3,7,5]
Output: []
Explanation: No even integers can be formed using the given digits.


Constraints:

        3 <= digits.length <= 100
        0 <= digits[i] <= 9
"""


class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        perms = set(
            (
                int("".join(str(y) for y in x))
                for x in permutations(set(digits), 3)
                if x[0] != 0
            )
        )
        return [x for x in sorted(perms) if x % 2 == 0]


sol = Solution()
res = sol.findEvenNumbers(digits=[2, 1, 3, 0])
assert res == [102, 120, 130, 132, 210, 230, 302, 310, 312, 320]
TLE = [
    7,
    1,
    2,
    3,
    7,
    1,
    3,
    0,
    6,
    9,
    3,
    6,
    2,
    5,
    8,
    3,
    7,
    2,
    4,
    8,
    7,
    6,
    6,
    8,
    8,
    1,
    5,
    7,
    3,
    5,
    6,
    0,
    4,
    4,
    0,
    0,
    1,
    9,
    1,
    3,
    4,
    2,
    8,
    9,
    4,
    6,
    9,
    3,
    2,
    1,
    2,
    8,
    2,
    9,
    5,
    4,
    3,
    2,
    5,
    5,
    5,
    7,
    2,
    0,
    0,
    4,
    3,
    8,
    4,
    0,
    1,
    1,
    7,
    8,
    4,
    9,
    9,
    9,
    6,
    1,
    8,
    5,
    5,
    5,
    6,
    7,
    0,
    3,
    6,
    0,
    1,
    2,
    4,
    7,
    9,
    8,
    9,
    0,
    6,
    7,
]
res = sol.findEvenNumbers(digits=TLE)
# print(res)
