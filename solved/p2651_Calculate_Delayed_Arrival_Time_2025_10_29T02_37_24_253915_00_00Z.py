"""
URL: https://leetcode.com/problems/calculate-delayed-arrival-time/description/?envType=problem-list-v2&envId=vn57k9wr

2651. Calculate Delayed Arrival Time

You are given a positive integer arrivalTime denoting the arrival time of a train in hours, and another positive integer delayedTime denoting the amount of delay in hours.

Return the time when the train will arrive at the station.

Note that the time in this problem is in 24-hours format.


Example 1:

Input: arrivalTime = 15, delayedTime = 5
Output: 20
Explanation: Arrival time of the train was 15:00 hours. It is delayed by 5 hours. Now it will reach at 15+5 = 20 (20:00 hours).

Example 2:

Input: arrivalTime = 13, delayedTime = 11
Output: 0
Explanation: Arrival time of the train was 13:00 hours. It is delayed by 11 hours. Now it will reach at 13+11=24 (Which is denoted by 00:00 in 24 hours format so return 0).


Constraints:

    1 <= arrivalTime < 24
    1 <= delayedTime <= 24
"""


class Solution:
    def findDelayedArrivalTime(self, arrivalTime: int, delayedTime: int) -> int:
        return (arrivalTime + delayedTime) % 24


sol = Solution()

# print(sol.findDelayedArrivalTime(15, 5))  # 20

assert sol.findDelayedArrivalTime(15, 5) == 20
assert sol.findDelayedArrivalTime(13, 11) == 0
assert sol.findDelayedArrivalTime(1, 1) == 2
assert sol.findDelayedArrivalTime(1, 24) == 1
assert sol.findDelayedArrivalTime(23, 1) == 0
assert sol.findDelayedArrivalTime(23, 24) == 23
assert sol.findDelayedArrivalTime(23, 23) == 22
assert sol.findDelayedArrivalTime(12, 12) == 0
assert sol.findDelayedArrivalTime(22, 3) == 1
