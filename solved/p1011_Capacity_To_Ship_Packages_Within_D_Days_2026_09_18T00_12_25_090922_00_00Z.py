"""
URL: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/description/?envType=problem-list-v2&envId=vn57k9wr

1011. Capacity To Ship Packages Within D Days

A conveyor belt has packages that must be shipped from one port to another within days days.

The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

Example 1:

Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.

Example 2:

Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4

Example 3:

Input: weights = [1,2,3,1,1], days = 4
Output: 3
Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1

Constraints:

    1 <= days <= weights.length <= 5 * 10^4
    1 <= weights[i] <= 500
"""


class Solution:

    def shipWithinDays(self, weights: List[int], days: int) -> int:

        def can_ship(cap):
            splits = 1
            total = 0
            for w in weights:
                if w > cap:
                    return False
                if total + w > cap:
                    total = w
                    splits += 1
                else:
                    total += w
            return splits <= days

        return first_true(0, sum(weights), can_ship)


sol = Solution()

print(sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
assert sol.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
assert sol.shipWithinDays([1, 2, 3, 1, 1], 4) == 3

assert sol.shipWithinDays([500] * 50000, 1) == 25000000
assert sol.shipWithinDays([1] * 50000, 50000) == 1
assert sol.shipWithinDays([1] * 50000, 1) == 50000
assert sol.shipWithinDays([1, 500, 1, 500, 1, 500], 3) == 501
assert sol.shipWithinDays([100, 100, 100, 100, 100], 5) == 100
assert sol.shipWithinDays([100, 100, 100, 100, 100], 1) == 500
assert sol.shipWithinDays([1, 2, 3, 4, 5], 5) == 5
assert sol.shipWithinDays([5, 4, 3, 2, 1], 2) == 9
assert sol.shipWithinDays([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 3) == 4
assert sol.shipWithinDays([500, 1, 500, 1, 500, 1, 500], 4) == 501
assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 10
assert sol.shipWithinDays([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 1) == 55
