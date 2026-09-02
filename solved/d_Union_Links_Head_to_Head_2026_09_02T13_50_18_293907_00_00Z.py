"""
DRILL: Union Links Head to Head
TRAINS: union-find
SNIPPET: lcunionunion

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

A person's head is the employee you land on after
that walk - the one who is their own manager.

You are given two things. Do not build them.

    parent - the manager list, already filled in
    find   - a function. find(x) returns the current head
             of employee x by walking parent.

────────────────────────────────────────────────────────
Company policy - mergers
────────────────────────────────────────────────────────
Two employees can request a merger: their two companies
become one.

The rule is simple, and it is the whole drill:

    never reassign the two employees.
    ask find for each person's head, then hang one head
    under the other.

Direction (so the picture is checkable):

    A's head now reports to B's head.

If they already share a head, do nothing - they are
already the same company.

────────────────────────────────────────────────────────
Why not attach the employees themselves?
────────────────────────────────────────────────────────
Suppose you have two companies and you call union(0, 3)
on the two people at the bottom:

    2              5
    |              |
    1              4
    |              |
    0              3

    parent = [1, 2, 2, 4, 5, 5]
              0  1  2  3  4  5

WRONG - parent[0] = 3  (person 0 now reports to person 3):

    2              5
    |              |
    1              4
                   |
    0 ------------ 3

    0 left company 2. 1 still reports to 2.
    Coworkers 0 and 1 no longer share a head. The tree is broken.

RIGHT - parent[2] = 5  (head 2 now reports to head 5):

           5
          / \\
         2   4
         |   |
         1   3
         |
         0

    parent = [1, 2, 5, 4, 5, 5]
              0  1  2  3  4  5
                    ^
                    only this slot flipped

    The leaves did not move. Everyone under 2 still reports
    up through 2, and 2 now sits under 5. One company.

────────────────────────────────────────────────────────
What you must implement
────────────────────────────────────────────────────────

    def buildUnion(
        self,
        parent: list[int],
        find: Callable[[int], int],
    ) -> Callable[[int, int], bool]:

Return one thing:

    union - a function that, given employees a and b,
            hangs A's head under B's head (or does nothing
            if they already share a head).

The test suite will rewire entries in parent to build
chains, then call union on LEAVES, not heads. If you
attach the leaves, the asserts fail.

────────────────────────────────────────────────────────
Required implementation style
────────────────────────────────────────────────────────
- Do not create parent. Do not write find.
- union(a, b):
    ra = find(a)
    rb = find(b)
    if they differ, set parent[ra] = rb.
    if they are the same, leave parent alone.

────────────────────────────────────────────────────────
Worked example 1 - two people
────────────────────────────────────────────────────────

    parent = [0, 1]
    union = buildUnion(parent, find)

    0     1

    union(0, 1)          # find(0) is 0, find(1) is 1
                         # 0 now reports to 1

    1
    |
    0
    parent = [1, 1]

────────────────────────────────────────────────────────
Worked example 2 - two chains, merge the leaves
────────────────────────────────────────────────────────

    parent = [0, 1, 2, 3, 4, 5]
    union = buildUnion(parent, find)
    parent[0] = 1
    parent[1] = 2
    parent[3] = 4
    parent[4] = 5
    # parent is now [1, 2, 2, 4, 5, 5]

    2              5
    |              |
    1              4
    |              |
    0              3

    union(0, 3)          # find(0) is 2, find(3) is 5
                         # hang 2 under 5

           5
          / \\
         2   4
         |   |
         1   3
         |
         0

    parent = [1, 2, 5, 4, 5, 5]

────────────────────────────────────────────────────────
Worked example 3 - already the same company
────────────────────────────────────────────────────────

    2         3
    |
    1
    |
    0
    parent = [1, 2, 2, 3]

    union(0, 1)          # find(0) is 2, find(1) is 2
                         # same head - do nothing

    picture unchanged
    parent unchanged     [1, 2, 2, 3]

────────────────────────────────────────────────────────
Worked example 4 - two mergers, then merge the companies
────────────────────────────────────────────────────────

    0     1     2     3
    parent = [0, 1, 2, 3]

    union(0, 1)

    1     2     3
    |
    0
    parent = [1, 1, 2, 3]

    union(2, 3)

    1     3
    |     |
    0     2
    parent = [1, 1, 3, 3]

    union(0, 2)          # leaves again
                         # find(0) is 1, find(2) is 3
                         # hang 1 under 3

        3
       / \\
      1   2
      |
      0
    parent = [1, 3, 3, 3]

────────────────────────────────────────────────────────
Constraints
────────────────────────────────────────────────────────
1 <= n <= 1000
When union is called, the current parent list is guaranteed
to be free of cycles.
"""


class Solution:
    def buildUnion(
        self,
        parent: list[int],
        find: Callable[[int], int],
    ) -> Callable[[int, int], bool]:
        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra != rb:
                parent[ra] = rb

        return union


sol = Solution()


def setup(n):
    parent = [*range(n)]

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    union = sol.buildUnion(parent, find)
    return parent, union


print(sol.buildUnion([0, 1], lambda x: x))  # a union(a, b) function

# example 1 - two people
parent, union = setup(2)
assert parent == [0, 1]
union(0, 1)
assert parent == [1, 1]

# fresh singletons, hang 0 under 1, leave 2 and 3 alone
parent, union = setup(4)
union(0, 1)
assert parent == [1, 1, 2, 3]

# hang 2 under 0
parent, union = setup(4)
union(2, 0)
assert parent == [0, 1, 0, 3]

# example 2 - two chains, union the leaves
parent, union = setup(6)
parent[0] = 1
parent[1] = 2
parent[3] = 4
parent[4] = 5
assert parent == [1, 2, 2, 4, 5, 5]
union(0, 3)
assert parent == [1, 2, 5, 4, 5, 5]

# example 3 - already the same company
parent, union = setup(4)
parent[0] = 1
parent[1] = 2
union(0, 1)
assert parent == [1, 2, 2, 3]

# union with self is a no-op
parent, union = setup(3)
union(0, 0)
assert parent == [0, 1, 2]

# example 4 - two mergers, then merge the companies via leaves
parent, union = setup(4)
union(0, 1)
assert parent == [1, 1, 2, 3]
union(2, 3)
assert parent == [1, 1, 3, 3]
union(0, 2)
assert parent == [1, 3, 3, 3]

n = 1
parent, union = setup(1)
union(0, 0)
assert parent == [0]
