"""
URL: https://leetcode.com/problems/guess-number-higher-or-lower/description/?envType=study-plan-v2&envId=leetcode-75

374. Guess Number Higher or Lower

We are playing the Guess Game. The game is as follows:

I pick a number from 1 to n. You have to guess which number I picked (the number I picked stays the same throughout the game).

Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

You call a pre-defined API int guess(int num), which returns three possible results:

        -1: Your guess is higher than the number I picked (i.e. num > pick).
        1: Your guess is lower than the number I picked (i.e. num < pick).
        0: your guess is equal to the number I picked (i.e. num == pick).

Return the number that I picked.


Example 1:

Input: n = 10, pick = 6
Output: 6

Example 2:

Input: n = 1, pick = 1
Output: 1

Example 3:

Input: n = 2, pick = 1
Output: 1


Constraints:

        1 <= n <= 231 - 1
        1 <= pick <= n
"""


def guess(num):
    global pick
    if num > pick:
        return -1
    elif num < pick:
        return 1
    else:
        return 0


class Solution:
    def guessNumber(self, n: int) -> int:
        left, right = 0, n
        while left <= right:
            mid = (left + right) // 2
            res = guess(mid)
            if res == -1:
                right = mid - 1
            elif res == 1:
                left = mid + 1
            else:
                return mid


# Test cases
pick = 6
n = 10
sol = Solution()
assert sol.guessNumber(n) == 6

pick = 1
n = 1
assert sol.guessNumber(n) == 1

pick = 1
n = 2
assert sol.guessNumber(n) == 1

pick = 2
n = 2
assert sol.guessNumber(n) == 2

pick = 1
n = 1000000000
assert sol.guessNumber(n) == 1

pick = 1000000000
n = 1000000000
assert sol.guessNumber(n) == 1000000000
