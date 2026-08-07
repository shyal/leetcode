"""
URL: https://leetcode.com/problems/divisor-game/description/?envType=problem-list-v2&envId=vn57k9wr

1025. Divisor Game

Alice and Bob take turns playing a game, with Alice starting first.

Initially, there is a number n on the chalkboard. On each player's turn, that
player makes a move consisting of:

    - Choosing any integer x with 0 < x < n and n % x == 0.
    - Replacing the number n on the chalkboard with n - x.

Also, if a player cannot make a move, they lose the game.

Return true if and only if Alice wins the game, assuming both players play
optimally.


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
"""


class Solution:
    def divisorGame(self, n: int) -> bool:
        return n % 2 == 0


sol = Solution()

print(sol.divisorGame(2))  # True

assert sol.divisorGame(2) == True
assert sol.divisorGame(3) == False
assert sol.divisorGame(1) == False
assert sol.divisorGame(4) == True
assert sol.divisorGame(5) == False
assert sol.divisorGame(6) == True
assert sol.divisorGame(7) == False
assert sol.divisorGame(9) == False
assert sol.divisorGame(12) == True
assert sol.divisorGame(25) == False
assert sol.divisorGame(100) == True
assert sol.divisorGame(997) == False
assert sol.divisorGame(999) == False
assert sol.divisorGame(1000) == True

def brute_force(n, memo={}):
    if n in memo:
        return memo[n]
    result = any(not brute_force(n - x) for x in range(1, n) if n % x == 0)
    memo[n] = result
    return result

# for i in range(1, 101):
#     assert sol.divisorGame(i) == brute_force(i)