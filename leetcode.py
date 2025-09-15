from typing import List

"""
1037 - Valid Boomerang

Given an array points where points[i] = [xi, yi] represents a point on the X-Y plane, return true if these points are a boomerang.
A boomerang is a set of three points that are all distinct and not in a straight line.

Example 1:

Input: points = [[1,1],[2,3],[3,2]]
Output: true
Example 2:

Input: points = [[1,1],[2,2],[3,3]]
Output: false


Constraints:

points.length == 3
points[i].length == 2
0 <= xi, yi <= 100


# Notes:

This isn't the slop, it's the inverse. 

Todo: Revisit with cross multiplication.

"""


class Solution:
    def isBoomerang(self, points: List[List[int]]) -> bool:
        non_overlapping = all(a != b for a, b in zip(points, points[1:]))

        def get_slope(a, b):
            if a[0] == b[0]:
                return float("-inf")
            elif a[1] == b[1]:
                return float("inf")
            else:
                return (a[0] - b[0]) / (a[1] - b[1])

        slopes = [get_slope(a, b) for a, b in zip(points, points[1:])]
        return non_overlapping and slopes[0] != slopes[1]


sol = Solution()
assert sol.isBoomerang([[1, 1], [2, 3], [3, 2]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 3]]) == False
assert sol.isBoomerang([[0, 1], [0, 2], [1, 2]]) == True
assert sol.isBoomerang([[0, 2], [2, 1], [0, 0]]) == True
assert sol.isBoomerang([[0, 0], [0, 0], [1, 1]]) == False
assert sol.isBoomerang([[0, 0], [0, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [0, 1], [0, 2]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [2, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 2]]) == False
assert sol.isBoomerang([[1, 2], [3, 4], [5, 6]]) == False
assert sol.isBoomerang([[-1, 0], [0, 0], [1, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 3]]) == True
assert sol.isBoomerang([[0, 0], [0, 1], [1, 0]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 4]]) == True
assert sol.isBoomerang([[-1, -1], [0, 0], [1, 2]]) == True
assert sol.isBoomerang([[100, 100], [200, 200], [300, 301]]) == True
assert sol.isBoomerang([[0, 1], [1, 0], [2, 0]]) == True
assert sol.isBoomerang([[1, 0], [1, 1], [1, 2]]) == False
assert sol.isBoomerang([[2, 2], [3, 3], [1, 1]]) == False


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
