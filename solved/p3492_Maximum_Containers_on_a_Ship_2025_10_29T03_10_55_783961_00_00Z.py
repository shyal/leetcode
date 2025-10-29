"""
URL: https://leetcode.com/problems/maximum-containers-on-a-ship/description/?envType=problem-list-v2&envId=vn57k9wr

3492. Maximum Containers on a Ship

You are given a positive integer n representing an n x n cargo deck on a ship. Each cell on the deck can hold one container with a weight of exactly w.

However, the total weight of all containers, if loaded onto the deck, must not exceed the ship's maximum weight capacity, maxWeight.

Return the maximum number of containers that can be loaded onto the ship.

Example 1:

Input: n = 2, w = 3, maxWeight = 15
Output: 4
Explanation: The deck has 4 cells, and each container weighs 3. The total weight of loading all containers is 12, which does not exceed maxWeight.

Example 2:

Input: n = 3, w = 5, maxWeight = 20
Output: 4
Explanation: The deck has 9 cells, and each container weighs 5. The maximum number of containers that can be loaded without exceeding maxWeight is 4.

Constraints:

    1 <= n <= 1000
    1 <= w <= 1000
    1 <= maxWeight <= 10^9

---
They gave the answer in the 'hints' but this is a good example of a question i would have stumbled upon; that would have taken me a while, because maths.
"""


class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return int(min(n * n, maxWeight / w))


sol = Solution()

# print(sol.maxContainers(2, 3, 15))  # 4

assert sol.maxContainers(2, 3, 15) == 4
assert sol.maxContainers(3, 5, 20) == 4
assert sol.maxContainers(1, 1, 1) == 1
assert sol.maxContainers(1, 2, 1) == 0
assert sol.maxContainers(1, 1, 2) == 1
assert sol.maxContainers(1000, 1, 1000000) == 1000000
assert sol.maxContainers(1000, 1, 1000001) == 1000000
assert sol.maxContainers(1000, 1000, 999) == 0
assert sol.maxContainers(1000, 1000, 1000) == 1
assert sol.maxContainers(2, 3, 5) == 1
assert sol.maxContainers(2, 3, 6) == 2
assert sol.maxContainers(3, 5, 25) == 5
assert sol.maxContainers(1000, 1, 1) == 1
assert sol.maxContainers(1000, 1, 1000000000) == 1000000
assert sol.maxContainers(1, 1000, 1000000000) == 1
assert sol.maxContainers(500, 2, 1000000) == 250000
