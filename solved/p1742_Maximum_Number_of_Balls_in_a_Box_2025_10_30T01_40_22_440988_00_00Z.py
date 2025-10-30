"""
URL: https://leetcode.com/problems/maximum-number-of-balls-in-a-box/description/?envType=problem-list-v2&envId=vn57k9wr

1742. Maximum Number of Balls in a Box

You are working in a ball factory where you have n balls numbered from lowLimit up to highLimit inclusive (i.e., n == highLimit - lowLimit + 1), and an infinite number of boxes numbered from 1 to infinity.

Your job at this factory is to put each ball in the box with a number equal to the sum of digits of the ball's number. For example, the ball number 321 will be put in the box number 3 + 2 + 1 = 6 and the ball number 10 will be put in the box number 1 + 0 = 1.

Given two integers lowLimit and highLimit, return the number of balls in the box with the most balls.

Example 1:

Input: lowLimit = 1, highLimit = 10
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  2 1 1 1 1 1 1 1 1 0  0  ...
Box 1 has the most number of balls with 2 balls.

Example 2:

Input: lowLimit = 5, highLimit = 15
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  1 1 1 1 2 2 1 1 1 0  0  ...
Boxes 5 and 6 have the most number of balls with 2 balls in each.

Example 3:

Input: lowLimit = 19, highLimit = 28
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 12 ...
Ball Count:  0 1 1 1 1 1 1 1 1 2  0  0  ...
Box 10 has the most number of balls with 2 balls.

Constraints:

    1 <= lowLimit <= highLimit <= 10^5

"""


class Solution:
    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        boxes = defaultdict(int)
        for ball in range(lowLimit, highLimit + 1):
            numBalls = sum(self.getDigits(ball))
            boxes[numBalls] += 1
        return max(boxes.values())


sol = Solution()

assert sol.countBalls(1, 10) == 2
assert sol.countBalls(5, 15) == 2
assert sol.countBalls(19, 28) == 2
assert sol.countBalls(1, 1) == 1
assert sol.countBalls(10, 10) == 1
assert sol.countBalls(1, 20) == 3
assert sol.countBalls(99, 101) == 1
assert sol.countBalls(99999, 100000) == 1
assert sol.countBalls(1, 30) == 4
assert sol.countBalls(49999, 50001) == 1
