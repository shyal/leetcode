"""
URL: https://leetcode.com/problems/find-minimum-time-to-reach-last-room-i/description/?envType=problem-list-v2&envId=vn57k9wr

3341. Find Minimum Time to Reach Last Room I

There is a dungeon with n x m rooms arranged as a grid.

You are given a 2D array moveTime of size n x m, where moveTime[i][j] represents the minimum time in seconds after which the room opens and can be moved to. You start from the room (0, 0) at time t = 0 and can move to an adjacent room. Moving between adjacent rooms takes exactly one second.

Return the minimum time to reach the room (n - 1, m - 1).

Two rooms are adjacent if they share a common wall, either horizontally or vertically.

Example 1:

Input: moveTime = [[0,4],[4,4]]
Output: 6
Explanation:
The minimum time required is 6 seconds.
- At time t == 4, move from room (0, 0) to room (1, 0) in one second.
- At time t == 5, move from room (1, 0) to room (1, 1) in one second.

Example 2:

Input: moveTime = [[0,0,0],[0,0,0]]
Output: 3
Explanation:
The minimum time required is 3 seconds.
- At time t == 0, move from room (0, 0) to room (1, 0) in one second.
- At time t == 1, move from room (1, 0) to room (1, 1) in one second.
- At time t == 2, move from room (1, 1) to room (1, 2) in one second.

Example 3:

Input: moveTime = [[0,1],[1,2]]
Output: 3

Constraints:

    2 <= n == moveTime.length <= 50
    2 <= m == moveTime[i].length <= 50
    0 <= moveTime[i][j] <= 10^9
"""


# mu 0.12
# class Solution
#   def minTimeToReach(moveTime: [[int]]) -> int
#     q = heap([(0, 0, 0, 0, 0)])
#     seen = set([])
#     while q
#       weight, t, m, r, c = q.pop()
#       if (r, c) == shape(moveTime, last_index=True)
#         return t + m
#       seen.add((r, c))
#       for rr, cc in nbrs(moveTime, r, c)
#         if (rr, cc) not in seen
#           q <- (moveTime[rr][cc] + weight, t + 1, max(moveTime[rr][cc], m), rr, cc)

def _down(h, i, before):
    (n, x) = (len(h), h[i])
    while (c := (2 * i + 1)) < n:
        if c + 1 < n and before(h[c + 1], h[c]):
            c += 1
        if not before(h[c], x):
            break
        h[i] = h[c]
        i = c
    h[i] = x


def _gt(a, b):
    return b < a


def _lt(a, b):
    return a < b


def _pop(h, before):
    last = h.pop()
    if not h:
        return last
    (top, h[0]) = (h[0], last)
    _down(h, 0, before)
    return top


def _up(h, i, before):
    x = h[i]
    while i:
        p = (i - 1) // 2
        if not before(x, h[p]):
            break
        h[i] = h[p]
        i = p
    h[i] = x


class heap:

    def __init__(self, items=(), type=min):
        self.before = _gt if type is max else _lt
        self.h = list(items)
        for i in reversed(range(len(self.h) // 2)):
            _down(self.h, i, self.before)

    def push(self, x):
        self.h.append(x)
        _up(self.h, len(self.h) - 1, self.before)
    append = push

    def pop(self):
        return _pop(self.h, self.before)

    def peek(self):
        return self.h[0]

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return iter(self.h)


def shape(*seqs, last_index=False):
    if len(seqs) == 1:
        (dims, x) = ([len(seqs[0])], seqs[0])
        while dims[-1] and isinstance(x[0], list):
            x = x[0]
            dims.append(len(x))
    else:
        dims = [len(s) for s in seqs]
    return tuple((d - 1 for d in dims)) if last_index else tuple(dims)


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def in_bounds(grid, r, c=None):
    if c is None:
        (r, c) = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def nbrs(grid, r, c=None, dirs=CARDINALS, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    if c is None:
        (r, c) = r
    eq = val if eq is None else eq
    for (dr, dc) in dirs:
        (nr, nc) = (r + dr, c + dc)
        if in_bounds(grid, nr, nc):
            if _holds(grid[nr][nc], eq, lt, lte, gt, gte):
                yield (nr, nc)


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


class Solution:
    def minTimeToReach(self, moveTime: list[list[int]]) -> int:
        _in_moveTime, moveTime = moveTime, Grid(moveTime)
        _w_moveTime = moveTime
        try:
            q = heap([(0, 0, 0, 0, 0)])
            seen = set([])
            while q:
                weight, t, m, r, c = q.pop()
                if (r, c) == shape(moveTime, last_index=True):
                    return t + m
                seen.add((r, c))
                for rr, cc in nbrs(moveTime, r, c):
                    if (rr, cc) not in seen:
                        q.append((moveTime[rr][cc] + weight, t + 1, max(moveTime[rr][cc], m), rr, cc))
        finally:
            _in_moveTime[:] = _w_moveTime


sol = Solution()
print(sol.minTimeToReach([[0, 4], [4, 4]]))
_l, _r = sol.minTimeToReach([[0, 4], [4, 4]]), 6
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minTimeToReach([[0, 0, 0], [0, 0, 0]]), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minTimeToReach([[0, 0], [0, 0]]), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minTimeToReach([[0, 10], [10, 10]]), 12
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minTimeToReach([[0, -1], [-1, 0]]), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))


# FAILED: walked away after 21m 58s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
