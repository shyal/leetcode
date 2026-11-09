"""
EPI 18.2 Paint a Boolean matrix

Given a 2D list image of booleans and a cell at row x and column y, flip
the value of every cell in the region of (x, y). The region is the set of
cells with the value of (x, y) that (x, y) reaches through cells of that
value, moving between cells that share a side. Change image in place and
return nothing.

Example 1:

Input: image = [[True, False, False],
                [True, True, False],
                [False, True, True]], x = 0, y = 1
Output: image becomes [[True, True, True],
                       [True, True, True],
                       [False, True, True]]
Explanation: the region of (0, 1) is (0, 1), (0, 2) and (1, 2). The
cell (2, 0) is also False, but it shares a side only with True cells.

Example 2:

Input: image = [[True]], x = 0, y = 0
Output: image becomes [[False]]

Constraints:

    1 <= len(image) <= 100
    1 <= len(image[0]) <= 100
    0 <= x < len(image), 0 <= y < len(image[0])

    REQUIRED: O(rows * cols) time. NO recursion.
"""


class Solution:
    def flip_color(self, x: int, y: int, image: list[list[bool]]) -> None:
        pass


sol = Solution()

image = [[True, False, False], [True, True, False], [False, True, True]]
sol.flip_color(0, 1, image)
print(image)  # [[True, True, True], [True, True, True], [False, True, True]]

# bits = lambda *rows: [[c == "1" for c in r] for r in rows]
# img = bits("100", "110", "011")
# sol.flip_color(0, 1, img)
# assert img == bits("111", "111", "011")
# img = [[True]]
# sol.flip_color(0, 0, img)
# assert img == [[False]]
# img = bits("100", "110", "011")
# sol.flip_color(2, 0, img)
# assert img == bits("100", "110", "111")
# img = bits("100", "110", "011")
# sol.flip_color(2, 2, img)
# assert img == bits("000", "000", "000")
# img = bits("101", "010", "101")
# sol.flip_color(1, 1, img)
# assert img == bits("101", "000", "101")
# img = bits("10", "01")
# sol.flip_color(0, 0, img)
# assert img == bits("00", "01")
# img = bits("11011")
# sol.flip_color(0, 4, img)
# assert img == bits("11000")
# img = bits("0", "0", "1", "0")
# sol.flip_color(0, 0, img)
# assert img == bits("1", "1", "1", "0")
# img = [[True] * 100 for _ in range(100)]
# sol.flip_color(50, 50, img)
# assert img == [[False] * 100 for _ in range(100)]
# img = [[j == 50 for j in range(100)] for i in range(100)]
# sol.flip_color(0, 0, img)
# assert img == [[True] * 50 + [True] + [False] * 49 for _ in range(100)]
# img = [[i % 2 == 0 or j == (99 if i % 4 == 1 else 0) for j in range(100)] for i in range(99)]
# sol.flip_color(98, 99, img)
# assert img == [[False] * 100 for _ in range(99)]
