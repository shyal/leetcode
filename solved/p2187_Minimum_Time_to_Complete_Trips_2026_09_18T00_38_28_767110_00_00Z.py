"""
URL: https://leetcode.com/problems/minimum-time-to-complete-trips/description/?envType=problem-list-v2&envId=vn57k9wr

2187. Minimum Time to Complete Trips

You are given an array time where time[i] denotes the time taken by the iᵗʰ bus to complete one trip.

Each bus can make multiple trips successively; that is, the next trip can start immediately after completing the current trip. Also, each bus operates independently; that is, the trips of one bus do not influence the trips of any other bus.

You are also given an integer totalTrips, which denotes the number of trips all buses should make in total. Return the minimum time required for all buses to complete at least totalTrips trips.

Example 1:

Input: time = [1,2,3], totalTrips = 5
Output: 3
Explanation:
- At time t = 1, the number of trips completed by each bus are [1,0,0].
  The total number of trips completed is 1 + 0 + 0 = 1.
- At time t = 2, the number of trips completed by each bus are [2,1,0].
  The total number of trips completed is 2 + 1 + 0 = 3.
- At time t = 3, the number of trips completed by each bus are [3,1,1].
  The total number of trips completed is 3 + 1 + 1 = 5.
So the minimum time needed for all buses to complete at least 5 trips is 3.

Example 2:

Input: time = [2], totalTrips = 1
Output: 2
Explanation:
There is only one bus, and it will complete its first trip at t = 2.
So the minimum time needed to complete 1 trip is 2.

Constraints:

    1 <= time.length <= 10^5
    1 <= time[i], totalTrips <= 10^7
"""


class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        if totalTrips == 0:
            return 1

        def trips(t):
            return sum(t // x for x in time)

        return first_true(0, sum(time) * totalTrips, lambda x: trips(x) >= totalTrips)


sol = Solution()

print(sol.minimumTime([1, 2, 3], 5))  # 3

assert sol.minimumTime([1, 2, 3], 5) == 3
assert sol.minimumTime([2], 1) == 2

assert sol.minimumTime([1], 1) == 1
assert sol.minimumTime([1], 10**7) == 10000000
assert sol.minimumTime([10**7], 1) == 10000000
assert sol.minimumTime([10**7], 10**7) == 100000000000000
assert sol.minimumTime([1, 1, 1, 1, 1], 10**7) == 2000000
assert sol.minimumTime([2, 2, 2, 2], 10**7) == 5000000
assert sol.minimumTime([1, 2, 2, 3, 3, 3], 15) == 6
assert sol.minimumTime([3, 3, 3, 3, 3], 1) == 3
assert sol.minimumTime([5], 5) == 25
assert sol.minimumTime([1, 2, 3, 4, 5], 0) == 1
assert sol.minimumTime([1, 2, 3, 4, 5], 1) == 1
assert sol.minimumTime([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 100) == 10
