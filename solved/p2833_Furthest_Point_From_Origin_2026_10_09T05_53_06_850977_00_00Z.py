"""
URL: https://leetcode.com/problems/furthest-point-from-origin/description/?envType=problem-list-v2&envId=vn57k9wr

2833. Furthest Point From Origin

You are given a string moves of length n consisting only of characters 'L', 'R', and '_'. The string represents your movement on a number line starting from the origin 0.

In the iᵗʰ move, you can choose one of the following directions:

- move to the left if moves[i] = 'L' or moves[i] = '_'
- move to the right if moves[i] = 'R' or moves[i] = '_'

Return the distance from the origin of the furthest point you can get to after n moves.

Example 1:

Input: moves = "L_RL__R"
Output: 3
Explanation: The furthest point we can reach from the origin 0 is point -3 through the following sequence of moves "LLRLLLR".

Example 2:

Input: moves = "_R__LL_"
Output: 5
Explanation: The furthest point we can reach from the origin 0 is point -5 through the following sequence of moves "LRLLLLL".

Example 3:

Input: moves = "_______"
Output: 7
Explanation: The furthest point we can reach from the origin 0 is point 7 through the following sequence of moves "RRRRRRR".

Constraints:

    1 <= moves.length == n <= 50
    moves consists only of characters 'L', 'R' and '_'.

---

LEETCODE: Accepted (0 ms, 18.9 MB)
"""


# mu 0.7
# def furthestDistanceFromOrigin(moves: str) -> int
#   abs(moves.count("L") - moves.count('R')) + moves.count("_")

class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        return abs(moves.count("L") - moves.count('R')) + moves.count("_")


sol = Solution()
print(sol.furthestDistanceFromOrigin('L_RL__R'))
_l, _r = sol.furthestDistanceFromOrigin('L_RL__R'), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.furthestDistanceFromOrigin('_R__LL_'), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.furthestDistanceFromOrigin('_______'), 7
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('R'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('_'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L' * 50), 50
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('R' * 50), 50
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('_' * 50), 50
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLR'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_L_R_'), 28
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLR_'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L' * 25 + 'R' * 25), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L' * 24 + 'R' * 25 + '_'), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().furthestDistanceFromOrigin('L' * 10 + 'R' * 10 + '_' * 30), 30
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
