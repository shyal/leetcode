"""
URL: https://leetcode.com/problems/calculate-money-in-leetcode-bank/description/?envType=problem-list-v2&envId=vn57k9wr

1716. Calculate Money in Leetcode Bank

Hercy wants to save money for his first car. He puts money in the Leetcode bank every day.

He starts by putting in $1 on Monday, the first day. Every day from Tuesday to Sunday, he will put in $1 more than the day before. On every subsequent Monday, he will put in $1 more than the previous Monday.

Given n, return the total amount of money he will have in the Leetcode bank at the end of the nth day.


Example 1:

Input: n = 4
Output: 10
Explanation: After the 4th day, the total is 1 + 2 + 3 + 4 = 10.

Example 2:

Input: n = 10
Output: 37
Explanation: After the 10th day, the total is (1 + 2 + 3 + 4 + 5 + 6 + 7) + (2 + 3 + 4) = 37. Notice that on the 2nd Monday, Hercy only puts in $2.

Example 3:

Input: n = 20
Output: 96
Explanation: After the 20th day, the total is (1 + 2 + 3 + 4 + 5 + 6 + 7) + (2 + 3 + 4 + 5 + 6 + 7 + 8) + (3 + 4 + 5 + 6 + 7 + 8) = 96.


Constraints:

    1 <= n <= 1000

"""


class Solution:
    def totalMoney(self, n: int) -> int:
        amount = 0
        total = 0
        start = 0
        for i in range(n):
            if i % 7 == 0:
                start += 1
                amount = start
            else:
                amount += 1
            total += amount
        return total


sol = Solution()

# print(sol.totalMoney(4))  # 10

assert sol.totalMoney(4) == 10
assert sol.totalMoney(10) == 37
assert sol.totalMoney(20) == 96
assert sol.totalMoney(1) == 1
assert sol.totalMoney(2) == 3
assert sol.totalMoney(6) == 21
assert sol.totalMoney(7) == 28
assert sol.totalMoney(8) == 30
assert sol.totalMoney(13) == 55
assert sol.totalMoney(14) == 63
assert sol.totalMoney(15) == 66
assert sol.totalMoney(21) == 105
assert sol.totalMoney(1000) == 74926
