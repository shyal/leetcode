"""
URL: https://leetcode.com/problems/divisor-game/description/?envType=problem-list-v2&envId=vn57k9wr

1025. Divisor Game

Alice and Bob take turns playing a game, with Alice starting first.

Initially, there is a number n on the chalkboard. On each player's turn, that player makes a move consisting of:

- Choosing any integer x with 0 < x < n and n % x == 0.
- Replacing the number n on the chalkboard with n - x.

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
---
Both players want to win, which involves getting the last move.
So look at all numbers divisible by x, and pick the one so that
n - x > 0

LEETCODE: Accepted (0 ms, 19 MB)
"""


# mu 0.12
# class Solution
#   def divisorGame(n: int) -> bool
#     even(n)

def even(n):
    return n % 2 == 0


class Solution:
    def divisorGame(self, n: int) -> bool:
        return even(n)


sol = Solution()
print(sol.divisorGame(2))
_l, _r = sol.divisorGame(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.divisorGame(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.divisorGame(1), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(1000), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(999), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(4), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(5), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(10), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(11), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(0), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(998), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(997), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(500), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.divisorGame(501), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
