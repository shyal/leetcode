"""
URL: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/description/?envType=study-plan-v2&envId=leetcode-75

1011. Capacity To Ship Packages Within D Days

A conveyor belt has a number of packages that must be shipped from one port to another. The packages have weights given in an array weights, where weights[i] is the weight of the ith package.

We want to determine the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

The packages must be shipped in the order they appear in the array, without rearranging them. Each day, we load the ship with packages sequentially until we cannot load the next package without exceeding the capacity.

Return the minimum capacity required to ship all packages within days days.


Example 1:

Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1,2,3,4,5
2nd day: 6,7
3rd day: 8
4th day: 9
5th day: 10
Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2,3,4,5), (1,6,7), (8), (9), (10) is not allowed.

Example 2:

Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days: 3,2,2 in the first day, 4,1 in the second day, and 4 in the third day.

Example 3:

Input: weights = [1,2,3,1,1], days = 4
Output: 3


Constraints:

    1 <= days <= weights.length <= 5 * 10^4
    1 <= weights[i] <= 500

---

self.daysToShipPackages(weights, 15) is the function we can use to compute how many days
it'll take to ship packages for this given weight.

So we can perform a binary search by starting with a high number. The starting number
can by the sum of the array, which would essentially mean we can ship all the packages
in a single day.

This is essentially the number we are trying to minimize.

So self.daysToShipPackages(weights, sum(weights)) returns 1

Our minimum value for weightPerShipment should be the max size of a package in weights,
since else a package wouldn't fit any shipment.

Ugh ok this is frustrating. I know i'm very close, but somehow some tests don't pass.
I typically get confused in these minimization binary search problems
that involve increasing or decreasing values, knowing when to stop
what to return etc.

Must revisit.

"""


class Solution:

    def daysToShipPackages(self, nums, weightPerShipment):
        total = 0
        count = 0
        for n in nums:
            if n > weightPerShipment:
                return float("inf")
            if total + n >= weightPerShipment:
                count += 1
                total = n
            else:
                total += n
        return count

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        min_weight, max_weight = max(weights), sum(weights)
        while min_weight <= max_weight:
            guessWeight = (min_weight + max_weight) // 2
            daysToShip = self.daysToShipPackages(weights, guessWeight)
            if daysToShip >= days:
                min_weight = guessWeight + 1
            else:
                max_weight = guessWeight - 1
        return min_weight - 1


sol = Solution()

# print(sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
assert sol.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
# assert sol.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
assert sol.shipWithinDays([1], 1) == 1
assert sol.shipWithinDays([1, 2, 3], 1) == 6
# assert sol.shipWithinDays([1, 2, 3], 3) == 3
assert sol.shipWithinDays([500, 500, 500], 2) == 1000
assert sol.shipWithinDays([1, 1, 1, 1], 2) == 2
assert sol.shipWithinDays([1, 1, 1, 1], 1) == 4
assert sol.shipWithinDays([1, 1, 1, 1], 4) == 1
assert sol.shipWithinDays([5, 3, 2, 1], 2) == 6
assert sol.shipWithinDays([2, 2, 2, 2, 2], 3) == 4
# assert sol.shipWithinDays([1, 1, 1, 10], 2) == 10
assert sol.shipWithinDays([10, 1, 1, 1], 2) == 10
assert sol.shipWithinDays([1, 2, 3, 4], 2) == 6
assert sol.shipWithinDays([100], 1) == 100
assert sol.shipWithinDays([1, 1], 1) == 2
assert sol.shipWithinDays([1, 1], 2) == 1
assert sol.shipWithinDays([4, 5, 4, 5], 2) == 9
assert sol.shipWithinDays([3, 3, 3], 3) == 3
assert sol.shipWithinDays([3, 3, 3], 1) == 9
