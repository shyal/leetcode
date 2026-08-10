"""
URL: https://leetcode.com/problems/nearest-exit-from-entrance-in-maze/description/?envType=problem-list-v2&envId=vn57k9wr

1926. Nearest Exit from Entrance in Maze

You are given an m x n matrix maze (0-indexed) with empty cells (represented
as '.') and walls (represented as '+'). You are also given the entrance of
the maze, where entrance = [entrance_row, entrance_col] denotes the row and
column of the cell you are initially standing at.

In one step, you can move one cell up, down, left, or right. You cannot step
into a cell with a wall, and you cannot step outside the maze. Your goal is
to find the nearest exit from the entrance. An exit is defined as an empty
cell that is at the border of the maze. The entrance does not count as an
exit.

Return the number of steps in the shortest path from the entrance to the
nearest exit, or -1 if no such path exists.


Example 1:

Input: maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]
Output: 1
Explanation: There are 3 exits in this maze at [1,0], [0,2], and [2,3].
Initially, you are at the entrance cell [1,2].
- You can reach [1,0] by moving 2 steps left.
- You can reach [0,2] by moving 1 step up.
It is impossible to reach [2,3] from the entrance.
Thus, the nearest exit is [0,2], which is 1 step away.

Example 2:

Input: maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]
Output: 2
Explanation: There is 1 exit in this maze at [1,2].
[1,0] does not count as an exit since it is the entrance cell.
Initially, you are at the entrance cell [1,0].
- You can reach [1,2] by moving 2 steps right.
Thus, the nearest exit is [1,2], which is 2 steps away.

Example 3:

Input: maze = [[".","+"]], entrance = [0,0]
Output: -1
Explanation: There are no exits in this maze.


Constraints:

    maze.length == m
    maze[i].length == n
    1 <= m, n <= 100
    maze[i][j] is either '.' or '+'.
    entrance.length == 2
    0 <= entrance_row < m
    0 <= entrance_col < n
    entrance will always be an empty cell.

    
---

maze = [
["+","+",".","+"],
[".",".",".","+"],
["+","+","+","."]
],
entrance = [1,2]

"""


class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        q = deque([(entrance[0], entrance[1], 0)])
        last_row = len(maze) -1
        last_col = len(maze[0]) - 1
        while q:
            current = q.popleft()
            row, col, steps = current
            if maze[row][col] != '+':
                on_the_edge = ((row == 0 or row == last_row) or (col == 0 or col == last_col))
                is_entrance = (row == entrance[0] and col == entrance[1])
                if on_the_edge and not is_entrance:
                    return steps
                maze[row][col] = '+'
                if row > 0 and maze[row-1][col] != '+':
                    q.append((row-1, col, steps+1))
                if row < len(maze)-1 and maze[row+1][col] != '+':
                    q.append((row+1, col, steps+1))
                if col > 0 and maze[row][col-1] != '+':
                    q.append((row, col-1, steps+1))
                if col < len(maze[0]) - 1 and maze[row][col+1] != '+':
                    q.append((row, col+1, steps+1))
        return -1


sol = Solution()

# print(sol.nearestExit([["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]], [1, 2]))  # 1

assert sol.nearestExit([["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]], [1, 2]) == 1
assert sol.nearestExit([["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]], [1, 0]) == 2
assert sol.nearestExit([[".", "+"]], [0, 0]) == -1
assert sol.nearestExit([["."]], [0, 0]) == -1
assert sol.nearestExit([[".", "."]], [0, 0]) == 1
assert sol.nearestExit([["+", "+", "+"], ["+", ".", "+"], ["+", "+", "+"]], [1, 1]) == -1
assert sol.nearestExit([["+", ".", "+"], ["+", ".", "+"], ["+", "+", "+"]], [0, 1]) == -1
assert sol.nearestExit([["+"], ["."], ["."], ["+"]], [1, 0]) == 1
assert sol.nearestExit([[".", ".", ".", ".", "."]], [0, 2]) == 1
assert sol.nearestExit([[".", ".", "."], [".", ".", "."], [".", ".", "."]], [1, 1]) == 1
assert sol.nearestExit(
    [["+", "+", "+", "+"], ["+", ".", ".", "+"], ["+", ".", ".", "+"], ["+", "+", ".", "+"]], [1, 1]
) == 3
assert sol.nearestExit(
    [
        ["+", "+", "+", "+", "+"],
        ["+", ".", ".", ".", "+"],
        ["+", ".", "+", ".", "+"],
        ["+", ".", ".", ".", "."],
        ["+", "+", "+", "+", "+"],
    ],
    [1, 1],
) == 5
assert sol.nearestExit([[".", ".", "+"], ["+", ".", "+"], ["+", ".", "."]], [0, 0]) == 1