"""
URL: https://leetcode.com/problems/escape-the-ghosts/description/?envType=problem-list-v2&envId=vn57k9wr

789. Escape The Ghosts

You are playing a simplified PAC-MAN game on an infinite 2-D grid. You start at the point [0, 0], and you are given a destination point target = [x_target, y_target] that you are trying to get to. There are several ghosts on the map with their starting positions given as a 2D array ghosts, where ghosts[i] = [x_i, y_i] represents the starting position of the i-th ghost. All inputs are integral coordinates.

Each turn, you and all the ghosts may independently choose to either move 1 unit in any of the four cardinal directions: north, east, south, or west, or stay still. All actions happen simultaneously.

You escape if and only if you can reach the target before any ghost reaches you. If you reach any square (including the target) at the same time as a ghost, it does not count as an escape.

Return true if it is possible to escape regardless of how the ghosts move, otherwise return false.

Example 1:

Input: ghosts = [[1,0],[0,3]], target = [0,1]
Output: true
Explanation: You can reach the destination (0, 1) after 1 turn, while the ghosts located at (1, 0) and (0, 3) cannot catch up with you.

Example 2:

Input: ghosts = [[1,0]], target = [2,0]
Output: false
Explanation: You need to reach the destination (2, 0), but the ghost at (1, 0) lies between you and the destination.

Example 3:

Input: ghosts = [[2,0]], target = [1,0]
Output: false
Explanation: The ghost can reach the target at the same time as you.

Constraints:

    1 <= ghosts.length <= 100
    ghosts[i].length == 2
    -10^4 <= x_i, y_i <= 10^4
    There can be multiple ghosts in the same location.
    target.length == 2
    -10^4 <= x_target, y_target <= 10^4
---
So one needs to define the read of the ghosts, which is their starting position extended to in each cardinal direction
mark those, either as filled, or as lines. Then perform a BFS from pacman's start position, and see whether it can
reach the target location without crossing a ghost line.

hmm but since all actions happen simultaenously, this is a multi-source BFS.
the size of the grid is not defined, so we need to compute its extent first
or not

ok i was going in the wrong direction here with grid search:

used the wrong technique, so TLE. I was also assisted with the multi-bfs because sloppy
will revisit

So one needs to define the read of the ghosts, which is their starting position extended to in each cardinal direction
mark those, either as filled, or as lines. Then perform a BFS from pacman's start position, and see whether it can
reach the target location without crossing a ghost line.

hmm but since all actions happen simultaenously, this is a multi-source BFS.
the size of the grid is not defined, so we need to compute its extent first
or not

ok i was going in the wrong direction here with grid search:

used the wrong technique, so TLE. I was also assisted with the multi-bfs because sloppy
will revisit

LEETCODE: Wrong Answer (0/77 cases)
"""


# mu 0.10
# class Type
#   ghost = 0
#   pacman = 1
#   target = 2
#
# class Solution
#   def escapeGhosts(ghosts: [[int]], target: [int]) -> bool
#     q = deque()
#     grid = {:() -> {:int}}
#     grid[0][0] = Type.pacman
#     grid[target[0]][target[1]] = Type.target
#     for gr, gc in ghosts
#       if [gr, gc] == target
#         return False
#       q <- (gr, gc, Type.ghost)
#       grid[gr][gc] = Type.ghost
#     seen = set()
#     q <- (0, 0, Type.pacman)
#     for d, (row, col, type) in levels(q, grid)
#       if [row, col] == target
#         print((['ghost', 'pacman'][type]), "reached target")
#         return type
#       for dr, dc in CARDINALS
#         nr, nc = row + dr, col + dc
#         if (nc, nr) not in seen
#           seen.add((nr, nc))
#           q <- (nr, nc, type)
#     return False

from collections import defaultdict


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def levels(q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None):

    def keep(x):
        v = x if grid is None else grid[x[0]][x[1]]
        if not _holds(v, eq, lt, lte, gt, gte) or (seen is not None and x in seen):
            return False
        if seen is not None:
            seen.add(x)
        return True
    d = 0
    while q:
        popped = (q.popleft() for _ in range(len(q)))
        if grouped:
            level = [x for x in popped if keep(x)]
            if level:
                yield (d, level)
        else:
            for x in popped:
                if keep(x):
                    yield (d, x)
        d += 1


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


class Type:
    ghost = 0
    pacman = 1
    target = 2


# mu 0.10
# class PacType
#   ghost = 0
#   pacman = 1
#   target = 2
#
# class Solution
#   def escapeGhosts(ghosts: [[int]], target: [int]) -> bool
#     q = deque()
#     grid = {:() -> {:int}}
#     grid[0][0] = PacType.pacman
#     grid[target[0]][target[1]] = PacType.target
#     for gr, gc in ghosts
#       if [gr, gc] == target
#         return False
#       q <- (gr, gc, PacType.ghost)
#       grid[gr][gc] = PacType.ghost
#     seen = set()
#     q <- (0, 0, PacType.pacman)
#     for d, (row, col, type) in levels(q, grid)
#       if [row, col] == target
#         print((['ghost', 'pacman'][type]), "reached target")
#         return type
#       for dr, dc in CARDINALS
#         nr, nc = row + dr, col + dc
#         if (nc, nr) not in seen
#           seen.add((nr, nc))
#           q <- (nr, nc, type)
#     return False

from collections import defaultdict


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def levels(q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None):

    def keep(x):
        v = x if grid is None else grid[x[0]][x[1]]
        if not _holds(v, eq, lt, lte, gt, gte) or (seen is not None and x in seen):
            return False
        if seen is not None:
            seen.add(x)
        return True
    d = 0
    while q:
        popped = (q.popleft() for _ in range(len(q)))
        if grouped:
            level = [x for x in popped if keep(x)]
            if level:
                yield (d, level)
        else:
            for x in popped:
                if keep(x):
                    yield (d, x)
        d += 1


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


class PacType:
    ghost = 0
    pacman = 1
    target = 2


class Solution:
    def escapeGhosts(self, ghosts: list[list[int]], target: list[int]) -> bool:
        _in_ghosts, ghosts = ghosts, Grid(ghosts)
        _w_ghosts = ghosts
        try:
            q = deque()
            grid = defaultdict(lambda: defaultdict(int))
            grid[0][0] = PacType.pacman
            grid[target[0]][target[1]] = PacType.target
            for gr, gc in ghosts:
                if [gr, gc] == target:
                    return False
                q.append((gr, gc, PacType.ghost))
                grid[gr][gc] = PacType.ghost
            seen = set()
            q.append((0, 0, PacType.pacman))
            for d, (row, col, type) in levels(q, grid):
                if [row, col] == target:
                    print((['ghost', 'pacman'][type]), "reached target")
                    return type
                for dr, dc in CARDINALS:
                    nr, nc = row + dr, col + dc
                    if (nc, nr) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc, type))
            return False
        finally:
            _in_ghosts[:] = _w_ghosts


sol = Solution()
print(sol.escapeGhosts([[1, 0], [0, 3]], [0, 1]))
_l, _r = sol.escapeGhosts([[1, 0], [0, 3]], [0, 1]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[1, 0]], [2, 0]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[2, 0]], [1, 0]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[0, 0]], [0, 0]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[0, 0]], [1, 1]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[1, 1], [1, 1], [1, 1]], [2, 2]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[0, 1], [1, 0]], [1, 1]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[0, 0], [0, 0], [0, 0]], [0, 1]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.escapeGhosts([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [19, 20]], [20, 20]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
