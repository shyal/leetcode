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

This went a lot smoother this time, thanks for the binary search template.

"""


class Solution:

    def daysToShipPackages(self, nums, weightPerShipment):
        days = 1
        total = 0
        for n in nums:
            if total + n > weightPerShipment:
                days += 1
                total = n
            else:
                total += n
        return days

    # @viz_binary_search()
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        low = max(weights)
        high = sum(weights)
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            if self.daysToShipPackages(weights, mid) <= days:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if is_minimization:
                    low = mid + 1
                else:
                    high = mid - 1

        return result


sol = Solution()

# print(sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

assert sol.daysToShipPackages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 7
assert sol.daysToShipPackages([1, 1], 1) == 2
assert sol.daysToShipPackages([10, 10], 11) == 2
assert sol.daysToShipPackages([10, 10], 19) == 2
assert sol.daysToShipPackages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15) == 5
assert sol.daysToShipPackages([1, 2, 3], 5) == 2
assert sol.daysToShipPackages([1, 2, 3], 6) == 1
assert sol.daysToShipPackages([1, 2, 3, 1], 6) == 2

assert sol.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
assert sol.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
assert sol.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
assert sol.shipWithinDays([1], 1) == 1
assert sol.shipWithinDays([1, 2, 3], 1) == 6
assert sol.shipWithinDays([1, 2, 3], 3) == 3
assert sol.shipWithinDays([500, 500, 500], 2) == 1000
assert sol.shipWithinDays([1, 1, 1, 1], 2) == 2
assert sol.shipWithinDays([1, 1, 1, 1], 1) == 4
assert sol.shipWithinDays([1, 1, 1, 1], 4) == 1
assert sol.shipWithinDays([5, 3, 2, 1], 2) == 6
assert sol.shipWithinDays([2, 2, 2, 2, 2], 3) == 4
assert sol.shipWithinDays([1, 1, 1, 10], 2) == 10
assert sol.shipWithinDays([10, 1, 1, 1], 2) == 10
assert sol.shipWithinDays([1, 2, 3, 4], 2) == 6
assert sol.shipWithinDays([100], 1) == 100
assert sol.shipWithinDays([1, 1], 1) == 2
assert sol.shipWithinDays([1, 1], 2) == 1
assert sol.shipWithinDays([4, 5, 4, 5], 2) == 9
assert sol.shipWithinDays([3, 3, 3], 3) == 3
assert sol.shipWithinDays([3, 3, 3], 1) == 9
