# URL: https://leetcode.com/problems/create-grid-with-exactly-one-path/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3963. Create Grid With Exactly One Path
#
# You are given two integers m and n, representing the number of rows and columns of a grid.
#
# Construct any m x n grid consisting only of the characters '.' and '#', where:
#
# - '.' represents a free cell.
# - '#' represents an obstacle cell.
#
# A valid path is a sequence of free cells that:
# - Starts at the top-left cell (0, 0).
# - Ends at the bottom-right cell (m - 1, n - 1).
# - Moves only:
#   - Right, from (i, j) to (i, j + 1), or
#   - Down, from (i, j) to (i + 1, j).
#
# Return any grid such that there is exactly one valid path from the top-left cell to the bottom-right cell.
#
# Example 1:
#
# Input: m = 2, n = 3
# Output: ["..#","#.."]
# Explanation:
# The only valid path is: (0,0) -> (0,1) -> (1,1) -> (1,2)
#
# Example 2:
#
# Input: m = 3, n = 3
# Output: ["..#","#..","##."]
# Explanation:
# The only valid path is: (0,0) -> (0,1) -> (1,1) -> (1,2) -> (2,2)
#
# Example 3:
#
# Input: m = 1, n = 4
# Output: ["...."]
# Explanation:
# The only valid path is: (0,0) -> (0,1) -> (0,2) -> (0,3)
#
# Constraints:
#
#     1 <= m, n <= 25
#
# ---
# LEETCODE: Accepted (92 ms, 19.5 MB)

# mu 0.13

class Solution
  def createGrid(m: int, n: int) -> [str]
    grid = table(m, n, fill='#')
    seen = set([])
    q = deque([(0, 0, [[0, 0]])])
    while q
      r, c, path = q.popleft()
      if (r, c) in seen
        continue
      if (r, c) == (m-1, n-1)
        for a, b in path
          grid[a][b] = '.'
      seen.add((r, c))
      for rr, cc in [(1, 0), (0, 1)]
        rr += r
        cc += c
        if in_bounds(grid, rr, cc)
          q <- (rr, cc, path + [[rr, cc]])
    res = []
    for r in grid
      row = ''
      for x in r
        row += x
      res.append(row)
    res

sol = Solution()

# Example 1
print(sol.createGrid(2, 3))  # ["..#","#.."]

# assert sol.createGrid(2, 3) == ['..#', '#..']
# assert sol.createGrid(3, 3) == ['..#', '#..', '##.']
# assert sol.createGrid(1, 4) == ['....']
# assert sol.createGrid(1, 1) == ['.']
# assert sol.createGrid(25, 25) == ['.........................', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.', '########################.']
# assert sol.createGrid(1, 25) == ['.........................']
# assert sol.createGrid(25, 1) == ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
# assert sol.createGrid(2, 2) == ['..', '#.']
# assert sol.createGrid(3, 2) == ['..', '#.', '#.']
# assert sol.createGrid(0, 0) == []
# assert sol.createGrid(2, 3) == ['..#', '#..']
# assert sol.createGrid(7, 8) == ['........', '#######.', '#######.', '#######.', '#######.', '#######.', '#######.']
# assert sol.createGrid(4, 4) == ['....', '###.', '###.', '###.']
