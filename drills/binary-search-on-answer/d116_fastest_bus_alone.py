"""
DRILL: Fastest Bus Alone

Given an array time, where time[i] is the minutes bus i needs for one
trip, and an integer totalTrips, return the minute at which the fastest
bus, working alone, has completed totalTrips trips.

Example 1:

Input: time = [1, 2, 3], totalTrips = 5
Output: 5
Explanation: The fastest bus takes 1 minute per trip, so 5 trips take 5 minutes.

Example 2:

Input: time = [5], totalTrips = 5
Output: 25

Example 3:

Input: time = [3, 3, 3, 3, 3], totalTrips = 1
Output: 3

Constraints:

    1 <= len(time) <= 10^5
    1 <= time[i] <= 10^7
    1 <= totalTrips <= 10^7

    REQUIRED: must run in O(n) time. NO search. The returned minute
    must be enough for all buses together to complete totalTrips trips;
    a minute at which they have not is a fail.
"""


class Solution:

    def fastestAlone(self, time: List[int], totalTrips: int) -> int:
        pass


sol = Solution()

print(sol.fastestAlone([1, 2, 3], 5))  # 5

# assert sol.fastestAlone([1, 2, 3], 5) == 5
# assert sol.fastestAlone([5], 5) == 25
# assert sol.fastestAlone([3, 3, 3, 3, 3], 1) == 3
# assert sol.fastestAlone([2], 1) == 2
# assert sol.fastestAlone([10**7], 1) == 10**7
# assert sol.fastestAlone([10**7], 10**7) == 10**14
# assert sol.fastestAlone([4, 9, 2, 7], 3) == 6
# assert sol.fastestAlone([9, 8, 7, 6, 5], 4) == 20
