"""
URL: https://leetcode.com/problems/path-crossing/description/?envType=problem-list-v2&envId=vn57k9wr

1496. Path Crossing

Given a string path, where path[i] = 'N', 'S', 'E' or 'W', each representing
moving one unit north, south, east, or west, respectively. You start at the
origin (0, 0) on a 2D plane and walk on the path specified by path.

Return true if the path crosses itself at any point, that is, if at any time
you are on a location you have previously visited. Return false otherwise.


Example 1:

Input: path = "NES"
Output: false
Explanation: Notice that the path doesn't cross any point more than once.

Example 2:

Input: path = "NESWW"
Output: true
Explanation: Notice that the path visits the origin twice.


Constraints:

    1 <= path.length <= 10^4
    path[i] is either 'N', 'S', 'E', or 'W'.
"""


class Solution:
    def isPathCrossing(self, path: str) -> bool:
        D = dict(N=(0, 1), S=(0, -1), E=(1, 0), W=(-1, 0))
        visited = set([])
        pos = [0, 0]
        for p in path:
            visited.add(tuple(pos))
            pos[0] += D[p][0]
            pos[1] += D[p][1]
            if tuple(pos) in visited:
                return True
        return False




sol = Solution()

# print(sol.isPathCrossing("NES"))  # False

assert sol.isPathCrossing("NES") == False
assert sol.isPathCrossing("NESWW") == True
assert sol.isPathCrossing("N") == False
assert sol.isPathCrossing("S") == False
assert sol.isPathCrossing("E") == False
assert sol.isPathCrossing("W") == False
assert sol.isPathCrossing("NS") == True
assert sol.isPathCrossing("EW") == True
assert sol.isPathCrossing("WWEE") == True
assert sol.isPathCrossing("NESW") == True
assert sol.isPathCrossing("ENWS") == True
assert sol.isPathCrossing("NNSS") == True
assert sol.isPathCrossing("NEWS") == True
assert sol.isPathCrossing("NNESWW") == True
assert sol.isPathCrossing("NNEES") == False
assert sol.isPathCrossing("NNEESSW") == False
assert sol.isPathCrossing("NESSWWNNE") == True
assert sol.isPathCrossing("N" * 10000) == False
assert sol.isPathCrossing("N" * 5000 + "E" * 5000) == False
assert sol.isPathCrossing("N" * 5000 + "E" * 4999 + "W") == True