"""
URL: https://leetcode.com/problems/path-crossing/description/?envType=problem-list-v2&envId=vn57k9wr

1496. Path Crossing

Given a string path, where path[i] = 'N', 'S', 'E' or 'W', each representing moving one unit north, south, east, or west, respectively. You start at the origin (0, 0) on a 2D plane and walk on the path specified by path.

Return true if the path crosses itself at any point, that is, if at any time you are on a location you have previously visited. Return false otherwise.

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
        locs = set([(0, 0)])
        loc = [0, 0]
        for p in path:
            if p == "N":
                loc[1] += 1
            elif p == "S":
                loc[1] -= 1
            elif p == "E":
                loc[0] += 1
            elif p == "W":
                loc[0] -= 1
            if tuple(loc) in locs:
                return True
            locs.add(tuple(loc))
        return False


sol = Solution()

# print(sol.isPathCrossing("NES"))  # false

# assert sol.isPathCrossing("NES") == False
assert sol.isPathCrossing("NESWW") == True
# assert sol.isPathCrossing("N") == False
# assert sol.isPathCrossing("NS") == True
# assert sol.isPathCrossing("SSN") == True
# assert sol.isPathCrossing("EEEE") == False
# assert sol.isPathCrossing("EW") == True
# assert sol.isPathCrossing("NENWSE") == True
# assert sol.isPathCrossing("SWNE") == True
# assert sol.isPathCrossing("NNNEEE") == False
