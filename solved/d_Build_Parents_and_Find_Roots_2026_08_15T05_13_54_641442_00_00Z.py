"""
DRILL: Build Parents and Find Roots
TRAINS: union-find

This drill is the "find" half of union-find.

Imagine a company with n employees labeled 0 .. n-1.
Every employee has exactly one manager, recorded in a list called `parent`:
    parent[i] = the manager of employee i

Special case:
    if parent[i] == i, then employee i is a company head
    (they report to nobody above them).

Important guarantee:
    Management chains never contain cycles.
    Starting from any employee and repeatedly following
    "who is my manager?" will always eventually reach a head.

────────────────────────────────────────────────────────
What you must implement
────────────────────────────────────────────────────────

    def buildFind(self, n: int) -> tuple[list[int], Callable]:

You return two things:

1. parent  - a list of length n
2. find    - a function that, given an employee x,
             walks up the management chain until it
             finds a head and returns that head.

Initial state (what your function must set up):
    parent = [0, 1, 2, ..., n-1]
    i.e. every employee starts as their own head.

find(x) must always look at the *current* contents of parent.
The test suite (and the real company) will later change entries
in parent, for example:

    parent[1] = 0     # "employee 1 now reports to employee 0"

After any such change, find must still return the correct head
by following the new chain.

────────────────────────────────────────────────────────
Required implementation style
────────────────────────────────────────────────────────
- Create the parent list with a simple range.
- Implement find with a loop (or recursion) that hops
  parent[x] → parent[parent[x]] → … until it reaches
  someone who is their own manager.
- Path compression is optional; a plain hop is enough.

────────────────────────────────────────────────────────
Worked example (n = 4)
────────────────────────────────────────────────────────

Step 0 - just after buildFind(4)
    parent = [0, 1, 2, 3]

    Picture (everyone is a head):

        0     1     2     3

    find(2) → 2

Step 1 - reorganize
    parent[1] = 0
    parent[2] = 1
    parent is now [0, 0, 1, 3]

    Picture:

        0           3
        |
        1
        |
        2

    find(2) → 0     (2 → 1 → 0)
    find(1) → 0
    find(3) → 3

────────────────────────────────────────────────────────
Constraints
────────────────────────────────────────────────────────
1 ≤ n ≤ 1000
When find is called, the current parent list is guaranteed
to be free of cycles.
"""


class Solution:
    def buildFind(self, n: int):
        parent = [*range(n)]
        def find(x):
            if parent[x] == x:
                return x
            else:
                return find(parent[x])
        return parent, find


sol = Solution()

parent, find = sol.buildFind(4)
assert parent == [0, 1, 2, 3]
assert [find(x) for x in range(4)] == [0, 1, 2, 3]

parent[1] = 0
parent[2] = 1
assert find(2) == 0
assert find(1) == 0
assert find(3) == 3

parent, find = sol.buildFind(5)
parent[0] = 1
parent[1] = 2
parent[2] = 3
parent[3] = 4
assert find(0) == 4
assert find(4) == 4

parent, find = sol.buildFind(1)
assert find(0) == 0

print("All tests passed!")
