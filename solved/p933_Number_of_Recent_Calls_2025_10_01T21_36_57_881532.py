"""
URL: https://leetcode.com/problems/number-of-recent-calls/description/?envType=study-plan-v2&envId=leetcode-75

933. Number of Recent Calls

You have a RecentCounter class which counts the number of recent requests within a certain time frame.

Implement the RecentCounter class:

        RecentCounter() Initializes the counter with zero recent requests.
        int ping(int t) Adds a new request at time t, where t represents some time in milliseconds, and returns the number of requests that has happened in the past 3000 milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range [t - 3000, t].

It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.


Example 1:

Input
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
Output
[null, 1, 2, 3, 3]

Explanation
RecentCounter recentCounter = new RecentCounter();
recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3


Constraints:

        1 <= t <= 109
        Each test case will call ping with strictly increasing values of t.
        At most 104 calls will be made to ping.
"""

from collections import deque


class Solution:

    def main(self):
        class RecentCounter:

            def __init__(self):
                self.pings = deque()

            def ping(self, t: int) -> int:
                self.pings.append(t)
                while True:
                    if self.pings[0] < self.pings[-1] - 3000:
                        self.pings.popleft()
                    else:
                        break
                return len(self.pings)

        return RecentCounter


sol = Solution()
recentCounter = sol.main()()
assert recentCounter.ping(1) == 1
assert recentCounter.ping(100) == 2
assert recentCounter.ping(3001) == 3
assert recentCounter.ping(3002) == 3

recentCounter2 = sol.main()()
assert recentCounter2.ping(1) == 1
assert recentCounter2.ping(3001) == 2
assert recentCounter2.ping(6001) == 2
assert recentCounter2.ping(9001) == 2

recentCounter3 = sol.main()()
assert recentCounter3.ping(100) == 1
assert recentCounter3.ping(101) == 2
assert recentCounter3.ping(102) == 3
assert recentCounter3.ping(3103) == 1

recentCounter4 = sol.main()()
assert recentCounter4.ping(1) == 1
assert recentCounter4.ping(3000) == 2
assert recentCounter4.ping(3001) == 3
assert recentCounter4.ping(6001) == 2

recentCounter5 = sol.main()()
assert recentCounter5.ping(1000000000) == 1
assert recentCounter5.ping(1000000100) == 2
assert recentCounter5.ping(1000003001) == 2
assert recentCounter5.ping(1000030001) == 1

recentCounter6 = sol.main()()
assert recentCounter6.ping(1) == 1
assert recentCounter6.ping(3002) == 1
assert recentCounter6.ping(6003) == 1
