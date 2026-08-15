"""
DRILL: How Many Companies
TRAINS: union-find

Imagine a company with n employees labeled 0 .. n-1.
Every employee has exactly one manager, recorded in a list called `parent`:
    parent[i] = the manager of employee i

Special case:
    if parent[i] == i, then employee i is a company head
    (they report to nobody above them).

A person's head is who you land on after walking
"who is my manager?" until someone is their own manager.

You are given three things. Do not build them.

    parent - the manager list, already filled in.
             everyone starts as their own head:
             parent = [0, 1, 2, ..., n-1]
             so there are n companies at the start.

    find   - a function. find(x) returns the current head
             of employee x by walking parent.

    union  - a function. union(a, b) honors one fact:
             "a and b belong to the same company."
             It hangs A's head under B's head.
             Returns True  if two companies actually became one.
             Returns False if they already shared a head
             (the fact was already known - nothing merged).

You are also given a list of facts. Each fact is a pair
of employees who belong together. Nobody hands you the
companies. The groups are hidden inside the facts.

────────────────────────────────────────────────────────
The question
────────────────────────────────────────────────────────
After honoring every fact, how many companies exist?

A successful merge destroys exactly one company.
Start at n. Subtract 1 only when union returns True.

    count = n
    for a, b in facts:
        if union(a, b):
            count -= 1
    return count

A False union does not change the count.
They were already one company.

────────────────────────────────────────────────────────
Worked example 1 - a triangle and a loner
────────────────────────────────────────────────────────

    n = 4
    facts = [[0, 1], [0, 2], [1, 2]]

    start - 4 companies, everyone a head

        0     1     2     3

    fact (0, 1) - union returns True - count 3

        1     2     3
        |
        0

    fact (0, 2) - union returns True - count 2
    0's head is 1, 2's head is 2, hang 1 under 2

        2     3
        |
        1
        |
        0

    fact (1, 2) - already the same head - union
    returns False - count stays 2

        2     3
        |
        1
        |
        0

    answer: 2

────────────────────────────────────────────────────────
Worked example 2 - one chain
────────────────────────────────────────────────────────

    n = 3
    facts = [[0, 1], [1, 2]]

        0     1     2          start, 3

        1     2                after (0, 1), 2
        |
        0

        2                      after (1, 2), 1
        |
        1
        |
        0

    answer: 1

────────────────────────────────────────────────────────
Worked example 3 - a fact that changes nothing
────────────────────────────────────────────────────────

    n = 2
    facts = [[0, 1], [0, 1]]

        0     1                start, 2

        1                      after first (0, 1), 1
        |
        0

        1                      second (0, 1) is False, still 1
        |
        0

    answer: 1

────────────────────────────────────────────────────────
Worked example 4 - no facts
────────────────────────────────────────────────────────

    n = 5
    facts = []

        0     1     2     3     4

    nothing to honor. still 5 companies.

    answer: 5

────────────────────────────────────────────────────────
What you must implement
────────────────────────────────────────────────────────

    def countCompanies(
        self,
        parent: list[int],
        find: Callable[[int], int],
        union: Callable[[int, int], bool],
        facts: list[list[int]],
    ) -> int:

Return how many companies exist after honoring every fact.

────────────────────────────────────────────────────────
Required implementation style
────────────────────────────────────────────────────────
- Do not create parent. Do not write find. Do not write union.
- Start count at len(parent).
- For each fact, call union.
  Subtract 1 only when it returns True.
- Return the final count.
- Do not scan parent at the end. The count is maintained
  as you honor the facts.

────────────────────────────────────────────────────────
Constraints
────────────────────────────────────────────────────────
1 <= n <= 1000
0 <= len(facts) <= 2000
0 <= a, b < n
parent starts as [0, 1, ..., n-1]
"""


class Solution:
    def countCompanies(
        self,
        parent: list[int],
        find: Callable[[int], int],
        union: Callable[[int, int], bool],
        facts: list[list[int]],
    ) -> int:
        pass


sol = Solution()


def setup(n):
    parent = [*range(n)]

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    return parent, find, union


def companies(n, facts):
    parent, find, union = setup(n)
    return sol.countCompanies(parent, find, union, facts)


assert companies(4, [[0, 1], [0, 2], [1, 2]]) == 2
assert companies(3, [[0, 1], [1, 2]]) == 1
assert companies(5, []) == 5
assert companies(6, [[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == 1
assert companies(4, [[0, 1], [1, 0], [2, 3], [0, 3]]) == 1
assert companies(1, []) == 1
assert companies(2, [[0, 1], [0, 1]]) == 1
assert companies(4, [[0, 1], [2, 3]]) == 2
assert companies(3, [[0, 0]]) == 3

print("All tests passed!")
