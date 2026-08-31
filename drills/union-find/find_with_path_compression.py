"""
DRILL: Find with Path Compression
TRAINS: union-find
SNIPPET: lcunionfind

Imagine a company with n employees labeled 0 .. n-1.
Every employee has exactly one manager, recorded in a list called `parent`:
    parent[i] = the manager of employee i

Special case:
    if parent[i] == i, then employee i is a company head
    (they report to nobody above them).

Important guarantee:
    Management chains never contain cycles.
    Starting from any employee and repeatedly asking
    "who is my manager?" always reaches a head.

────────────────────────────────────────────────────────
Company policy – path compression
────────────────────────────────────────────────────────
Long reporting chains are slow.  Therefore, whenever find(x)
walks up a chain to discover the head, it *flattens* the chain
behind it:

    after reaching the head, every employee visited on the way
    is reassigned to report DIRECTLY to the head.

After that single call, the next find on any of those employees
is only one hop.  This flattening is called path compression.

Full compression is required:
    everyone on the walked path ends up pointing straight at the head,
    not merely one level higher.

Employees that were never visited stay exactly as they were.

────────────────────────────────────────────────────────
What you must implement
────────────────────────────────────────────────────────

    def buildFind(self, n: int) -> tuple[list[int], Callable]:

Return two things:

1. parent – a list of length n that starts as
            parent = [0, 1, 2, ..., n-1]
            (every employee begins as their own head)

2. find   – a function that, given an employee x,
            • returns the head that x ultimately reports to, and
            • compresses the entire path it just walked.

────────────────────────────────────────────────────────
Worked example (n = 5)
────────────────────────────────────────────────────────

Step 0 – build a long chain
    parent, find = buildFind(5)
    parent[0] = 1
    parent[1] = 2
    parent[2] = 3
    parent[3] = 4
    # parent is now [1, 2, 3, 4, 4]

    Picture before any find:

        4
        |
        3
        |
        2
        |
        1
        |
        0

Step 1 – call find(0)
    find walks  0 → 1 → 2 → 3 → 4  and returns 4.
    Having reached the head, it rewrites every parent entry on
    that path so they all point directly at the head:

        parent becomes [4, 4, 4, 4, 4]

    Picture after compression:

         _____4_____
        |   |   |   |
        0   1   2   3

    A second call find(0) is now a single hop.

────────────────────────────────────────────────────────
Constraints
────────────────────────────────────────────────────────
1 ≤ n ≤ 1000
When find is called, the current parent list is guaranteed
to be free of cycles.
"""


class Solution:
    def buildFind(self, n: int):
        pass


sol = Solution()

print(sol.buildFind(5))  # (parent, find): parent == [0, 1, 2, 3, 4]

# parent, find = sol.buildFind(5)
# parent[0] = 1
# parent[1] = 2
# parent[2] = 3
# parent[3] = 4
# assert find(0) == 4
# assert parent == [4, 4, 4, 4, 4]

# parent, find = sol.buildFind(7)
# parent[0] = 1
# parent[1] = 2
# parent[3] = 4
# parent[4] = 5
# assert find(0) == 2
# assert parent == [2, 2, 2, 4, 5, 5, 6]
# assert find(3) == 5
# assert parent == [2, 2, 2, 5, 5, 5, 6]

# parent, find = sol.buildFind(3)
# assert find(0) == 0
# assert parent == [0, 1, 2]

# parent, find = sol.buildFind(4)
# parent[1] = 0
# assert find(1) == 0
# assert parent == [0, 0, 2, 3]

# parent, find = sol.buildFind(1)
# assert find(0) == 0
# assert parent == [0]
