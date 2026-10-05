"""
URL: https://leetcode.com/problems/last-stone-weight/description/?envType=problem-list-v2&envId=vn57k9wr

1046. Last Stone Weight

You are given an array of integers stones where stones[i] is the weight of the iᵗʰ stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last remaining stone. If there are no stones left, return 0.

Example 1:

Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation:
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

Example 2:

Input: stones = [1]
Output: 1

Constraints:

    1 <= stones.length <= 30
    1 <= stones[i] <= 1000

---

LEETCODE: Accepted (4 ms, 19.7 MB)
"""


# mu 0.7
# def lastStoneWeight(stones: [int]) -> int
#   h = heap(stones, type=max)
#   while len(h.h) >= 2
#     x, y = h.pop(), h.pop()
#     x, y = [*sorted([x, y])]
#     if x == y
#       if len(h.h) == 0
#         return 0
#       continue
#     else
#       h.push(y - x)
#   return h.peek()

from heapq import heapify, heappop, heappush


class heap:
    class _Rev:
        __slots__ = "x"

        def __init__(self, x):
            self.x = x

        def __lt__(self, o):
            return o.x < self.x

    def __init__(self, items=(), type=min):
        self.rev = type is max
        self.h = [self.wrap(x) for x in items]
        heapify(self.h)

    def wrap(self, x):
        return heap._Rev(x) if self.rev else x

    def unwrap(self, x):
        return x.x if self.rev else x

    def push(self, x):
        heappush(self.h, self.wrap(x))

    append = push

    def pop(self):
        return self.unwrap(heappop(self.h))

    def peek(self):
        return self.unwrap(self.h[0])

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return (self.unwrap(x) for x in self.h)


class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        h = heap(stones, type=max)
        while len(h.h) >= 2:
            x, y = h.pop(), h.pop()
            x, y = [*sorted([x, y])]
            if x == y:
                if len(h.h) == 0:
                    return 0
                continue
            else:
                h.push(y - x)
        return h.peek()


sol = Solution()
print(sol.lastStoneWeight([2, 7, 4, 1, 8, 1]))
assert sol.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
assert sol.lastStoneWeight([1]) == 1
assert sol.lastStoneWeight([1, 1, 1, 1]) == 0
assert sol.lastStoneWeight([1000] * 30) == 0
assert sol.lastStoneWeight([1, 1000]) == 999
assert sol.lastStoneWeight([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]) == 0
assert sol.lastStoneWeight([2, 2, 3, 3, 4, 4, 5, 5]) == 0
assert sol.lastStoneWeight([1]) == 1
assert sol.lastStoneWeight([999, 1000]) == 1
assert sol.lastStoneWeight([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 1
assert sol.lastStoneWeight([10] * 15 + [9] * 15) == 1
assert sol.lastStoneWeight([1] * 29 + [2]) == 1
assert sol.lastStoneWeight([1000]) == 1000
assert sol.lastStoneWeight([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]) == 0
