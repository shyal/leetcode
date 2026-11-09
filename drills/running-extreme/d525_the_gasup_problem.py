"""
EPI 17.6 The gasup problem

Given lists gas and dist for n cities on a circular road, return the index
of an ample city. City i holds gas[i] gallons, and the road from city i to
city (i + 1) % n is dist[i] miles long. A car goes 20 miles on each gallon.
It starts at a city with an empty tank and takes all the gas of each city
it reaches, the start city included. A city is ample when the car can start
there and go once round the road, in the order of the indices, with no
negative amount of gas in the tank at any point. When several cities are
ample, return any of them.

Example 1:

Input: gas = [2, 1, 4, 3], dist = [60, 40, 20, 80]
Output: 2
Explanation: from city 2 the car has gas for 80 miles. It reaches city 3
with 60 left, city 0 with 60 + 60 - 80 = 40, city 1 with 40 + 40 - 60 = 20
and city 2 with 20 + 20 - 40 = 0. No other city is ample.

Example 2:

Input: gas = [5], dist = [100]
Output: 0

Example 3:

Input: gas = [1, 1], dist = [20, 20]
Output: 0
Explanation: both cities are ample, so 1 is also correct.

Constraints:

    1 <= n <= 10^5
    0 <= gas[i] <= 10^4
    1 <= dist[i] <= 10^5
    20 * sum(gas) >= sum(dist), so an ample city exists.

    REQUIRED: O(n) time and O(1) extra space.
"""


class Solution:
    def find_ample_city(self, gas: list[int], dist: list[int]) -> int:
        pass


sol = Solution()

print(sol.find_ample_city([2, 1, 4, 3], [60, 40, 20, 80]))  # 2

# ample = lambda gas, dist: (c := sol.find_ample_city(gas, dist)) in range(len(gas)) and min(accumulate(20 * gas[(c + k) % len(gas)] - dist[(c + k) % len(gas)] for k in range(len(gas)))) >= 0
# assert sol.find_ample_city([2, 1, 4, 3], [60, 40, 20, 80]) == 2
# assert ample([2, 1, 4, 3], [60, 40, 20, 80])
# assert ample([5], [100])
# assert ample([1, 1], [20, 20])
# assert sol.find_ample_city([0, 0, 0, 3], [20, 20, 10, 10]) == 3
# assert sol.find_ample_city([3, 0, 0, 0], [10, 20, 20, 10]) == 0
# assert ample([0, 0, 0, 3], [20, 20, 10, 10])
# assert ample([3, 0, 0, 0], [10, 20, 20, 10])
# assert ample([0, 2, 0, 2], [20, 20, 20, 20])
# assert ample([5, 0, 0, 0, 5], [40, 10, 10, 30, 10])
# assert ample([10, 0, 1, 0], [50, 50, 50, 50])
# assert ample([1, 2, 3, 4, 5], [100, 20, 20, 20, 20])
# assert ample([1] * 100000, [20] * 100000)
# assert sol.find_ample_city([0] * 99999 + [100000], [20] * 100000) == 99999
# assert sol.find_ample_city([100000] + [0] * 99999, [20] * 100000) == 0
# assert ample([2 * (i % 2) for i in range(100000)], [20] * 100000)
