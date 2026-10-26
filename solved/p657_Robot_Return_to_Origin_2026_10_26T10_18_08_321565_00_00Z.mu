# URL: https://leetcode.com/problems/robot-return-to-origin/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 657. Robot Return to Origin
#
# There is a robot starting at the position (0, 0), the origin, on a 2D plane. Given a sequence of its moves, judge if this robot ends up at (0, 0) after it completes its moves.
#
# You are given a string moves that represents the move sequence of the robot where moves[i] represents its iᵗʰ move. Valid moves are 'R' (right), 'L' (left), 'U' (up), and 'D' (down).
#
# Return true if the robot returns to the origin after it finishes all of its moves, or false otherwise.
#
# Note: The way that the robot is "facing" is irrelevant. 'R' will always make the robot move to the right once, 'L' will always make it move left, etc. Also, assume that the magnitude of the robot's movement is the same for each move.
#
# Example 1:
#
# Input: moves = "UD"
# Output: true
# Explanation: The robot moves up once, and then down once. All moves have the same magnitude, so it ended up at the origin where it started. Therefore, we return true.
#
# Example 2:
#
# Input: moves = "LL"
# Output: false
# Explanation: The robot moves left twice. It ends up two "moves" to the left of the origin. We return false because it is not at the origin at the end of its moves.
#
# Constraints:
#
#     1 <= moves.length <= 2 * 10^4
#     moves only contains the characters 'U', 'D', 'L' and 'R'.
#
# ---
# LEETCODE: Accepted (28 ms, 19.2 MB)

# mu 0.13

class Solution
  def judgeCircle(moves: str) -> bool
    dirs = dict(U=(0, 1), D=(0, -1), L=(-1, 0), R=(1, 0))
    pos = [0, 0]
    for dir in moves
      pos[0] += dirs[dir][0]
      pos[1] += dirs[dir][1]
    pos == [0, 0]

sol = Solution()

print(sol.judgeCircle('UD'))  # True

assert sol.judgeCircle('UD') is true
assert sol.judgeCircle('LL') is false

assert sol.judgeCircle('') == true
assert sol.judgeCircle('U' * 10000 + 'D' * 10000) == true
assert sol.judgeCircle('L' * 20000) == false
assert sol.judgeCircle('R' * 10000 + 'L' * 10000) == true
assert sol.judgeCircle('UDLR' * 5000) == true
assert sol.judgeCircle('U' * 9999 + 'D' * 10000) == false
assert sol.judgeCircle('UDUDUDUDUDUDUDUDUDUD') == true
assert sol.judgeCircle('LLLLRRRR') == true
assert sol.judgeCircle('UUUUDDDD') == true
assert sol.judgeCircle('UDLRUDLRUDLRUDLRUDLR') == true
assert sol.judgeCircle('U' * 20000) == false
assert sol.judgeCircle('D' * 20000) == false
