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


# mu 0.7
# def fewest(a: int, b: int, limit: int) -> int
#   q = deque([[0, a]])
#   seen = set()
#   while q
#     dist, v = q.popleft()
#     if (dist, v) in seen
#       continue
#     seen.add((dist, v))
#     if v < 0 or v > limit
#       continue
#     if v == b
#       return dist
#     q <- (dist + 1, (v + 1))
#     q <- (dist + 1, (v * 2))
#   return -1

class Solution:
    def fewest(self, a: int, b: int, limit: int) -> int:
        q = deque([[0, a]])
        seen = set()
        while q:
            dist, v = q.popleft()
            if (dist, v) in seen:
                continue
            seen.add((dist, v))
            if v < 0 or v > limit:
                continue
            if v == b:
                return dist
            q.append((dist + 1, (v + 1)))
            q.append((dist + 1, (v * 2)))
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
