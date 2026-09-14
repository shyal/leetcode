"""
DRILL: Clubs Sharing A Member

There are n clubs, numbered 0 to n - 1. Given n and clubs_of, where
clubs_of[p] is the list of clubs person p is in, two clubs are connected
when at least one person is in both. Return the adjacency list adj,
where adj[i] is the list of indexes of the clubs connected to club i, in
any order. A club is never connected to itself.

Example 1:

Input: n = 4, clubs_of = {51: [0], 53: [0, 2], 52: [1, 3], 54: [2, 3]}
Output: [[2], [3], [0, 3], [1, 2]]
Explanation: each circle is a club with its members inside. Person 53
is in clubs 0 and 2, person 54 in clubs 2 and 3, and person 52 in clubs
1 and 3.

     club 0        club 1        club 2        club 3
    .------.      .------.      .------.      .------.
   (  51 53  )   (   52    )   (  53 54  )   (  54 52  )
    '------'      '------'      '------'      '------'

Example 2:

Input: n = 3, clubs_of = {57: [0, 1, 2]}
Output: [[1, 2], [0, 2], [0, 1]]

Constraints:

    1 <= n <= 500
    1 <= len(clubs_of) <= 10^5
    sum(len(clubs_of[p])) <= 10^5
    0 <= person id < 10^6
    0 <= club index < n

    REQUIRED: must run in O(n * L) time, where n is the number of clubs
    and L is the total number of entries in clubs_of. NO person-to-person
    edges; NO element-by-element pair tests.

---

Learning

"""


class Solution:

    def clubGraph(self, n: int, clubs_of: Dict[int, List[int]]) -> List[List[int]]:
        adj = [set() for _ in range(n)]
        for clubs in clubs_of.values():
            for i in clubs:
                adj[i].update(clubs)
        for i in range(n):
            adj[i].discard(i)
        return adj


sol = Solution()

print(
    sol.clubGraph(4, {51: [0], 53: [0, 2], 52: [1, 3], 54: [2, 3]})
)  # [[2], [3], [0, 3], [1, 2]]

# assert same_rows(sol.clubGraph(4, {51: [0], 53: [0, 2], 52: [1, 3], 54: [2, 3]}), [[2], [3], [0, 3], [1, 2]])
# assert same_rows(sol.clubGraph(3, {57: [0, 1, 2]}), [[1, 2], [0, 2], [0, 1]])
# assert same_rows(sol.clubGraph(1, {58: [0]}), [[]])
# assert same_rows(sol.clubGraph(2, {51: [0], 52: [0], 53: [1], 54: [1]}), [[], []])
