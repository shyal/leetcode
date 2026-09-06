"""
DRILL: How Many Companies
TRAINS: union-find

Given n employees numbered 0 to n - 1 and facts, where facts[i] = [a, b]
means a and b work at the same company, return how many companies there
are once every fact is known. You are given find and union over the list
parent, where every employee starts as their own company. The call
union(a, b) merges the companies of a and b and returns True, or returns
False when they were already one company. Do not write find or union.

Example 1:

Input: n = 4, facts = [[0, 1], [0, 2], [1, 2]]
Output: 2
Explanation: 0, 1 and 2 are one company. 3 is another. The third fact
merges nothing.

Example 2:

Input: n = 5, facts = []
Output: 5

Constraints:

    1 <= n <= 1000
    0 <= len(facts) <= 2000
    facts[i] = [a, b] with 0 <= a, b < n
    parent starts as [0, 1, ..., n - 1]

    REQUIRED: must use only what union returns. NO scan of parent at the
    end. NO find or union of your own.
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


print(companies(4, [[0, 1], [0, 2], [1, 2]]))  # 2

# assert companies(4, [[0, 1], [0, 2], [1, 2]]) == 2
# assert companies(3, [[0, 1], [1, 2]]) == 1
# assert companies(5, []) == 5
# assert companies(6, [[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == 1
# assert companies(4, [[0, 1], [1, 0], [2, 3], [0, 3]]) == 1
# assert companies(1, []) == 1
# assert companies(2, [[0, 1], [0, 1]]) == 1
# assert companies(4, [[0, 1], [2, 3]]) == 2
# assert companies(3, [[0, 0]]) == 3
