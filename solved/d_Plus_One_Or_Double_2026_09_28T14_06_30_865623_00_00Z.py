"""
DRILL: Plus One Or Double
TRAINS: generate-and-test-neighbors

Given integers a, b and limit, return the fewest moves that turn a into b,
or -1 when no sequence of moves does. One move replaces x with x + 1 or
with 2 * x. Every value along the way must stay between 0 and limit.

Example 1:

Input: a = 3, b = 10, limit = 20
Output: 3
Explanation: 3 to 4 to 5 to 10. Doubling first reaches 6, then 12, and
12 can never come back down to 10.

Example 2:

Input: a = 10, b = 3, limit = 20
Output: -1
Explanation: No move makes a value smaller.

Example 3:

Input: a = 0, b = 1, limit = 1
Output: 1
Explanation: Doubling 0 gives 0 again. Only x + 1 leaves it.

Constraints:

    0 <= a, b <= limit <= 10^5

    REQUIRED: O(limit) time, one breadth-first search over values. Every
    reachable value is expanded once. NO greedy choice of the value nearest
    to b.
"""


# mu 0.6
# def fewest(a: int, b: int, limit: int) -> int
#   q = deque([a])
#   for (d, c) in levels(q, seen=set(), lte=limit)
#     if c == b
#       return d
#     for op in [c + 1, c * 2]
#       q.append(op)
#   -1

def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def levels(
    q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None
):
    bare = eq is None and lt is None and lte is None and gt is None and gte is None
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    d = 0
    while q:
        level = []
        for _ in range(len(q)):
            x = q.popleft()
            if seen is not None and x in seen:
                continue
            if not bare:
                v = x if grid is None else row(grid, x[0])[x[1]]
                if not _holds(v, eq, lt, lte, gt, gte):
                    continue
            if seen is not None:
                seen.add(x)
            if grouped:
                level.append(x)
            else:
                yield d, x
        if grouped and level:
            yield d, level
        d += 1


class Solution:
    def fewest(self, a: int, b: int, limit: int) -> int:
        q = deque([a])
        for (d, c) in levels(q, seen=set(), lte=limit):
            if c == b:
                return d
            for op in [c + 1, c * 2]:
                q.append(op)
        return -1


sol = Solution()
print(sol.fewest(3, 10, 20))
assert sol.fewest(3, 10, 20) == 3
assert sol.fewest(10, 3, 20) == -1
assert sol.fewest(0, 1, 1) == 1
assert sol.fewest(7, 7, 7) == 0
assert sol.fewest(0, 0, 0) == 0
assert sol.fewest(1, 1024, 1024) == 10
assert sol.fewest(1, 1024, 1023) == -1
assert sol.fewest(2, 9, 9) == 3
assert sol.fewest(1, 100000, 100000) == 21
