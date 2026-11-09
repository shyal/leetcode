"""
EPI 16.10 Count the number of moves to climb stairs

Given top, the number of stairs, and maximum_step, return the number of
ways to climb from the bottom to stair top when each move climbs 1 to
maximum_step stairs. Two ways are different when their lists of moves,
in order, are different.

Example 1:

Input: top = 4, maximum_step = 2
Output: 5
Explanation: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1 and 2+2.

Example 2:

Input: top = 3, maximum_step = 10
Output: 4
Explanation: 1+1+1, 1+2, 2+1 and 3. No move may go past stair 3.

Example 3:

Input: top = 1, maximum_step = 1
Output: 1

Constraints:

    1 <= top <= 1000
    1 <= maximum_step <= 50

    REQUIRED: O(top * maximum_step) time. NO enumeration of the lists of
    moves.
"""


class Solution:
    def number_of_ways_to_top(self, top: int, maximum_step: int) -> int:
        pass


sol = Solution()

print(sol.number_of_ways_to_top(4, 2))  # 5

# assert sol.number_of_ways_to_top(4, 2) == 5
# assert sol.number_of_ways_to_top(3, 10) == 4
# assert sol.number_of_ways_to_top(1, 1) == 1
# assert sol.number_of_ways_to_top(10, 1) == 1
# assert sol.number_of_ways_to_top(2, 2) == 2
# assert sol.number_of_ways_to_top(5, 5) == 16
# assert sol.number_of_ways_to_top(6, 3) == 24
# assert sol.number_of_ways_to_top(10, 3) == 274
# assert sol.number_of_ways_to_top(20, 4) == 283953
# assert sol.number_of_ways_to_top(30, 2) == 1346269
# assert sol.number_of_ways_to_top(50, 50) == 562949953421312
# assert sol.number_of_ways_to_top(100, 2) == 573147844013817084101
# assert sol.number_of_ways_to_top(1000, 1) == 1
# assert sol.number_of_ways_to_top(1000, 10) % 1000000007 == 858977721
# assert sol.number_of_ways_to_top(1000, 50) % 1000000007 == 438993203
