"""
URL: https://leetcode.com/problems/divisor-game/description/

1025. Divisor Game

Alice and Bob take turns playing a game, with Alice starting first.

Initially, there is a number n on the chalkboard. On each player's turn, that player makes a move consisting of:

    Choosing any x with 0 < x < n and n % x == 0.
    Replacing the number n on the chalkboard with n - x.

Also, if a player cannot make a move, they lose the game.

Return true if and only if Alice wins the game, assuming both players play optimally.


Example 1:

Input: n = 2
Output: true
Explanation: Alice chooses 1, and Bob has no more moves.

Example 2:

Input: n = 3
Output: false
Explanation: Alice chooses 1, Bob chooses 1, and Alice has no more moves.


Constraints:

    1 <= n <= 1000


---------

Had to look up the solution for this. It may or may not fall in the DP arena, as
one can also take a pure maths approach.
"""


class Solution:
    def divisorGame(self, n: int) -> bool:
        return n % 2 == 0


sol = Solution()
assert sol.divisorGame(2) == True
assert sol.divisorGame(3) == False
assert sol.divisorGame(4) == True
assert sol.divisorGame(8) == True
