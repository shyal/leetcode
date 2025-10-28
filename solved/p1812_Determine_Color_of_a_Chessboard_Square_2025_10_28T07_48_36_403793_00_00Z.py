"""
URL: https://leetcode.com/problems/determine-color-of-a-chessboard-square/description/?envType=problem-list-v2&envId=vn57k9wr

1812. Determine Color of a Chessboard Square

You are given coordinates, a string that represents the coordinates of a square of the chessboard. Below is a chessboard for your reference.

[Chessboard image]

Return true if the square is white, and false if the square is black.

The coordinate will always represent a valid chessboard square. The coordinate will always have the letter first, and the number second.


Example 1:

Input: coordinates = "a1"
Output: false
Explanation: From the chessboard above, the square with coordinates "a1" is black, so return false.

Example 2:

Input: coordinates = "h3"
Output: true
Explanation: From the chessboard above, the square with coordinates "h3" is white, so return true.

Example 3:

Input: coordinates = "c7"
Output: false


Constraints:

    coordinates.length == 2
    'a' <= coordinates[0] <= 'h'
    '1' <= coordinates[1] <= '8'
"""


class Solution:
    def squareIsWhite(self, coordinates: str) -> bool:
        col, row = coordinates
        col = (ord(col) - ord("a")) % 2 != 0
        row = (int(row) - 1) % 2 != 0
        return col ^ row


sol = Solution()

# print(sol.squareIsWhite("a1"))  # false

assert sol.squareIsWhite("a1") == False
assert sol.squareIsWhite("h3") == True
assert sol.squareIsWhite("c7") == False
assert sol.squareIsWhite("a8") == True
assert sol.squareIsWhite("h8") == False
assert sol.squareIsWhite("h1") == True
assert sol.squareIsWhite("b2") == False
assert sol.squareIsWhite("e4") == True
assert sol.squareIsWhite("d5") == True
assert sol.squareIsWhite("g7") == False
assert sol.squareIsWhite("f6") == False
