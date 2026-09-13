"""
DRILL: Clubs Sharing A Member

There are n clubs, numbered 0 to n - 1. Given n and members, where
members[i] is the list of ids of the people in club i, two clubs are
connected when at least one person is in both. Return the adjacency list
adj, where adj[i] is the list of indexes of the clubs connected to club
i, in increasing order. A club is never connected to itself.

Example 1:

Input: n = 4, members = [[51, 53], [52], [53, 54], [54, 52]]
Output: [[2], [3], [0, 3], [1, 2]]
Explanation: each circle is a club with its members inside. Person 53
is in clubs 0 and 2, person 54 in clubs 2 and 3, and person 52 in clubs
1 and 3.

     club 0        club 1        club 2        club 3
    .------.      .------.      .------.      .------.
   /        \    /        \    /        \    /        \
  |  51  53  |  |    52    |  |  53  54  |  |  54  52  |
   \        /    \        /    \        /    \        /
    '------'      '------'      '------'      '------'

Example 2:

Input: n = 3, members = [[57], [57], [57]]
Output: [[1, 2], [0, 2], [0, 1]]

Constraints:

    1 <= n <= 500
    len(members) == n
    1 <= len(members[i]) <= 10^5
    sum(len(members[i])) <= 10^5
    0 <= person id < 10^6

    REQUIRED: must run in O(n * L) time, where n is the number of clubs
    and L is the total number of member entries. NO person-to-person
    edges; NO element-by-element pair tests.
"""


class Solution:

    def clubGraph(self, n: int, members: List[List[int]]) -> List[List[int]]:
        pass


sol = Solution()

print(sol.clubGraph(4, [[51, 53], [52], [53, 54], [54, 52]]))  # [[2], [3], [0, 3], [1, 2]]

# assert sol.clubGraph(4, [[51, 53], [52], [53, 54], [54, 52]]) == [[2], [3], [0, 3], [1, 2]]
# assert sol.clubGraph(3, [[57], [57], [57]]) == [[1, 2], [0, 2], [0, 1]]
# assert sol.clubGraph(1, [[58]]) == [[]]
# assert sol.clubGraph(2, [[51, 52], [53, 54]]) == [[], []]
