"""
Given a square matrix friends, where friends[a][b] is 1 when users a and
b are friends and 0 otherwise, and two users userA and userB, return the
friend distance between them: the smallest number of friendships on a
chain of users from userA to userB. Return 0 when userA and userB are
the same user, and -1 when no chain joins them.

Example 1:

Input: friends = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]], userA = 0, userB = 2
Output: 2

    0 --- 1 --- 2

Explanation: user 0 and user 2 are not friends. Both are friends with
user 1, so the chain 0, 1, 2 has two friendships.

Example 2:

Input: friends = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]], userA = 0, userB = 1
Output: 1

Example 3:

Input: friends = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]], userA = 0, userB = 2
Output: -1

Constraints:

    1 <= len(friends) <= 1000
    friends[a][b] is 0 or 1, friends[a][b] == friends[b][a], friends[a][a] == 0
    0 <= userA, userB < len(friends)

    REQUIRED: O(n^2) time for n users. NO DFS. NO all-pairs distances.
"""


class Solution:
    def friend_distance(self, friends: list[list[int]], userA: int, userB: int) -> int:
        pass


sol = Solution()

draw_graphviz({0: [1], 1: [0, 2], 2: [1]})
print(sol.friend_distance([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 0, 2))  # 2

# assert sol.friend_distance([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 0, 2) == 2
# assert sol.friend_distance([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 0, 1) == 1
# assert sol.friend_distance([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 2) == -1
# assert sol.friend_distance([[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1], [0, 0, 0, 1, 0]], 0, 4) == 4
# assert sol.friend_distance([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 1, 1) == 0
# assert sol.friend_distance([[0]], 0, 0) == 0
# assert sol.friend_distance([[0, 1], [1, 0]], 1, 0) == 1
# assert sol.friend_distance([[0, 0], [0, 0]], 0, 1) == -1
# assert sol.friend_distance([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]], 0, 3) == 2
# assert sol.friend_distance([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]], 0, 2) == 2
# assert sol.friend_distance([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], 0, 3) == -1
# n = 1000
# chain = [[1 if abs(a - b) == 1 else 0 for b in range(n)] for a in range(n)]
# assert sol.friend_distance(chain, 0, n - 1) == n - 1
# assert sol.friend_distance(chain, n - 1, 0) == n - 1
# full = [[0 if a == b else 1 for b in range(n)] for a in range(n)]
# assert sol.friend_distance(full, 0, n - 1) == 1
