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

---

I'm having a bit of trouble understanding the actual question...

So we have packages that need to be shipped within `days`. e.g 5

Then we have package weights:

1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Oh right, so it's a trial and error thing, i guess.

If we pick a capacity of 15, then 1, 2, 3, 4, 5 ships in a day, then 6 and 7 etc.
so we can pick C (capacity), and get a binary, did we ship within the timeframe
or not.

Let's build the decision function first, then the binary search.


Sadly i'm over time now, because of a silly mistake in can_ship. So recognition was
fine, implementation of the BS was fine (i think) and it's just a silly arithmetic
problem of splitting an array by totals. Ridiculous.

Ok complete failure, both on the can_ship and the binary search.

"""


class Solution:

    def can_ship(self, weights, capacity, days):
        days_taken = 0
        total = 0
        for v in weights:
            if v > capacity:
                return False
            if total + v >= capacity:
                days_taken += 1
            else:
                total += v
        print(days_taken, days_taken <= days)
        return days_taken <= days

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        left, right = 0, sum(weights)
        vals = {}
        while left < right:
            mid = (left + right) // 2
            can_ship = self.can_ship(weights, mid, days)
            vals[mid] = can_ship
            if can_ship:
                right = mid
            else:
                left = mid + 1

        print([[k, vals[k]] for k in sorted(vals.keys())])

        return left


sol = Solution()

# print(sol.can_ship([1, 2, 3], 3, 1))  # False
# print(sol.can_ship([1, 2, 3], 3, 2))  # True
# print(sol.can_ship([1, 2, 3], 1, 2))  # False
# assert sol.can_ship([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 12, 5) == False
assert sol.can_ship([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15, 5) == True
# print(sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

# assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
# assert sol.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
# assert sol.shipWithinDays([1, 2, 3, 1, 1], 4) == 3

# assert sol.shipWithinDays([500] * 50000, 1) == 25000000
# assert sol.shipWithinDays([1] * 50000, 50000) == 1
# assert sol.shipWithinDays([1] * 50000, 1) == 50000
# assert sol.shipWithinDays([1, 500, 1, 500, 1, 500], 3) == 501
# assert sol.shipWithinDays([100, 100, 100, 100, 100], 5) == 100
# assert sol.shipWithinDays([100, 100, 100, 100, 100], 1) == 500
# assert sol.shipWithinDays([1, 2, 3, 4, 5], 5) == 5
# assert sol.shipWithinDays([5, 4, 3, 2, 1], 2) == 9
# assert sol.shipWithinDays([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 3) == 4
# assert sol.shipWithinDays([500, 1, 500, 1, 500, 1, 500], 4) == 501
# assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 10
# assert sol.shipWithinDays([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 1) == 55


# FAILED: walked away after 37m 20s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
