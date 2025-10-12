"""
URL: https://leetcode.com/problems/snake-in-matrix/description/?envType=problem-list-v2&envId=vn57k9wr

3248. Snake in Matrix

There is a snake in an n x n matrix grid and can move in four possible directions. Each cell in the grid is identified by the position: grid[i][j] = (i * n) + j.

The snake starts at cell 0 and follows a sequence of commands.

You are given an integer n representing the size of the grid and an array of strings commands where each command[i] is either "UP", "RIGHT", "DOWN", and "LEFT". It's guaranteed that the snake will remain within the grid boundaries throughout its movement.

Return the position of the final cell where the snake ends up after executing commands.


Example 1:

Input: n = 2, commands = ["RIGHT","DOWN"]

Output: 3

Explanation:

0123

0123

0123

Example 2:

Input: n = 3, commands = ["DOWN","RIGHT","UP"]

Output: 1

Explanation:

012345678

012345678

012345678

012345678


Constraints:

        2 <= n <= 10
        1 <= commands.length <= 100
        commands consists only of "UP", "RIGHT", "DOWN", and "LEFT".
        The input is generated such the snake will not move outside of the boundaries.
"""


class Solution:
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        deltas = dict(RIGHT=(0, 1), LEFT=(0, -1), UP=(-1, 0), DOWN=(1, 0))
        pos = reduce(
            lambda acc, val: (acc[0] + deltas[val][0], acc[1] + deltas[val][1]),
            commands,
            (0, 0),
        )
        return pos[0] * n + pos[1]


sol = Solution()

# print(sol.finalPositionOfSnake(n=2, commands=["RIGHT", "DOWN"]))
# print(sol.finalPositionOfSnake(n=3, commands=["DOWN", "RIGHT", "UP"]))

assert sol.finalPositionOfSnake(2, ["RIGHT", "DOWN"]) == 3
assert sol.finalPositionOfSnake(3, ["DOWN", "RIGHT", "UP"]) == 1
assert sol.finalPositionOfSnake(2, ["RIGHT"]) == 1
assert sol.finalPositionOfSnake(2, ["DOWN"]) == 2
assert sol.finalPositionOfSnake(2, ["DOWN", "RIGHT", "UP", "LEFT"]) == 0
assert sol.finalPositionOfSnake(3, ["RIGHT", "RIGHT"]) == 2
assert sol.finalPositionOfSnake(3, ["DOWN", "DOWN"]) == 6
assert sol.finalPositionOfSnake(3, ["DOWN", "RIGHT", "UP", "LEFT"]) == 0
assert sol.finalPositionOfSnake(10, ["RIGHT"] * 9) == 9
assert sol.finalPositionOfSnake(10, ["DOWN"] * 9) == 90
assert sol.finalPositionOfSnake(10, ["DOWN"] * 9 + ["RIGHT"] * 9) == 99
assert sol.finalPositionOfSnake(10, ["RIGHT", "LEFT"] * 50) == 0
assert sol.finalPositionOfSnake(10, ["DOWN", "UP"] * 50) == 0
