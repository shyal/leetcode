"""
1518. Water Bottles
Easy
Topics
premium lock icon
Companies
Hint
There are numBottles water bottles that are initially full of water. You can exchange numExchange empty water bottles from the market with one full water bottle.

The operation of drinking a full water bottle turns it into an empty bottle.

Given the two integers numBottles and numExchange, return the maximum number of water bottles you can drink.

 

Example 1:


Input: numBottles = 9, numExchange = 3
Output: 13
Explanation: You can exchange 3 empty bottles to get 1 full water bottle.
Number of water bottles you can drink: 9 + 3 + 1 = 13.
Example 2:


Input: numBottles = 15, numExchange = 4
Output: 19
Explanation: You can exchange 4 empty bottles to get 1 full water bottle. 
Number of water bottles you can drink: 15 + 3 + 1 = 19.
 

Constraints:

1 <= numBottles <= 100
2 <= numExchange <= 100
"""


class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        drink = numBottles
        remainder = 0
        while numBottles + remainder >= numExchange:
            numBottles, remainder = divmod(numBottles + remainder, numExchange)
            drink += numBottles
        return drink


sol = Solution()
assert sol.numWaterBottles(9, 3) == 13
assert sol.numWaterBottles(15, 4) == 19
assert sol.numWaterBottles(5, 3) == 7
assert sol.numWaterBottles(1, 2) == 1
assert sol.numWaterBottles(2, 2) == 3
assert sol.numWaterBottles(100, 2) == 199
assert sol.numWaterBottles(10, 5) == 12
assert sol.numWaterBottles(7, 3) == 10
assert sol.numWaterBottles(4, 3) == 5
assert sol.numWaterBottles(3, 3) == 4
assert sol.numWaterBottles(99, 100) == 99
assert sol.numWaterBottles(100, 100) == 101
assert sol.numWaterBottles(2, 3) == 2
assert sol.numWaterBottles(3, 2) == 5
assert sol.numWaterBottles(50, 5) == 62
assert sol.numWaterBottles(20, 6) == 23
assert sol.numWaterBottles(8, 4) == 10
