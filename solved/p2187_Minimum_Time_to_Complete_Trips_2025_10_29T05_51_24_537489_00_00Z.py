"""
URL: https://leetcode.com/problems/minimum-time-to-complete-trips/description/?envType=problem-list-v2&envId=vn57k9wr

2187. Minimum Time to Complete Trips

You are given an array time where time[i] denotes the time taken by the i-th bus to complete one trip.

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

---

Felt quite easy now, but maybe i got lucky.

"""


class Solution:

    def numTripsCompleted(self, time, totaltime):
        return sum(totaltime // t for t in time)

    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        # @viz_binary_search
        low = 1
        high = min(time) * totalTrips
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            if self.numTripsCompleted(time, mid) >= totalTrips:
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

# print(sol.numTripsCompleted([1, 2, 3], 3))
# print(sol.numTripsCompleted([2], 2))
# print(sol.minimumTime([1, 2, 3], 5))  # 3

assert sol.minimumTime([1, 2, 3], 5) == 3
assert sol.minimumTime([2], 1) == 2
assert sol.minimumTime([1], 1) == 1
assert sol.minimumTime([1], 10_000_000) == 10_000_000
assert sol.minimumTime([10_000_000], 1) == 10_000_000
assert sol.minimumTime([3, 3, 3], 4) == 6
assert sol.minimumTime([1, 2, 3], 10) == 6
assert sol.minimumTime([2, 3], 3) == 4
assert sol.minimumTime([1, 10000000], 2) == 2
assert sol.minimumTime([1, 10000000], 10000001) == 10000000
assert sol.minimumTime([1, 1, 1, 1, 1], 10) == 2
