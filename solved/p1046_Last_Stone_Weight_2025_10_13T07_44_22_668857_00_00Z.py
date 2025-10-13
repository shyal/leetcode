"""
URL: https://leetcode.com/problems/last-stone-weight/description/

1046. Last Stone Weight

You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

    If x == y, both stones are destroyed, and
    If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last remaining stone. If there are no stones left, return 0.


Example 1:

Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation: We combine 7 and 8 to get 1, so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2, so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1, so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0, so the array converts to [1] then that's the value of the last stone.

Example 2:

Input: stones = [1]
Output: 1


Constraints:

    1 <= stones.length <= 30
    1 <= stones[i] <= 1000

"""


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-x for x in stones]
        heapify(stones)
        # draw_heap(stones)
        while True:
            if len(stones) == 1:
                return -stones[0]
            elif len(stones) == 0:
                return 0
            y = -heappop(stones)
            x = -heappop(stones)
            if x == y:
                continue
            heappush(stones, -(y - x))


sol = Solution()

# print(sol.lastStoneWeight([2, 7, 4, 1, 8, 1]))  # 1

assert sol.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
assert sol.lastStoneWeight([1]) == 1
assert sol.lastStoneWeight([2, 2]) == 0
assert sol.lastStoneWeight([1, 3]) == 2
assert sol.lastStoneWeight([1, 1, 1]) == 1
assert sol.lastStoneWeight([3, 7, 2]) == 2
assert sol.lastStoneWeight([1000]) == 1000
assert sol.lastStoneWeight([1, 1, 1, 1, 1]) == 1
assert sol.lastStoneWeight([1, 1, 1, 1]) == 0
assert sol.lastStoneWeight([2, 4, 5]) == 1
assert sol.lastStoneWeight([4, 3, 4, 3, 2]) == 2
assert sol.lastStoneWeight([5, 5, 5]) == 5
assert sol.lastStoneWeight([1000] * 30) == 0
assert sol.lastStoneWeight([1000] * 29) == 1000
