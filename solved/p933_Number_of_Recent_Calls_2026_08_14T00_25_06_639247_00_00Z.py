"""
URL: https://leetcode.com/problems/number-of-recent-calls/description/?envType=problem-list-v2&envId=vn57k9wr

933. Number of Recent Calls

You have a RecentCounter class which counts the number of recent requests within
a certain time frame.

Implement the RecentCounter class:

    - RecentCounter() Initializes the counter with zero recent requests.
    - int ping(int t) Adds a new request at time t, where t represents some time
      in milliseconds, and returns the number of requests that has happened in
      the past 3000 milliseconds (including the new request). Specifically,
      return the number of requests that have happened in the inclusive range
      [t - 3000, t].

It is guaranteed that every call to ping uses a strictly larger value of t than
the previous call.


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

    1 <= t <= 10^9
    Each test case will call ping with strictly increasing values of t.
    At most 10^4 calls will be made to ping.
"""


class RecentCounter:
    def __init__(self):
        self.d = deque([])

    def ping(self, t: int) -> int:
        self.d.append(t)
        cut_off = t - 3000
        count = 0
        for v in self.d:
            if v < cut_off:
                count += 1
        for _ in range(count):
            self.d.popleft()
        return len(self.d)


obj = RecentCounter()

# print([obj.ping(t) for t in [1, 100, 3001, 3002]])  # [1, 2, 3, 3]

obj = RecentCounter()
assert obj.ping(1) == 1
assert obj.ping(100) == 2
assert obj.ping(3001) == 3
assert obj.ping(3002) == 3

obj = RecentCounter()
assert obj.ping(1) == 1

obj = RecentCounter()
assert obj.ping(1) == 1
assert obj.ping(3001) == 2
assert obj.ping(3002) == 2

obj = RecentCounter()
assert obj.ping(1) == 1
assert obj.ping(2) == 2
assert obj.ping(3) == 3
assert obj.ping(3003) == 2
assert obj.ping(3004) == 2
assert obj.ping(6004) == 2

obj = RecentCounter()
assert obj.ping(3000) == 1
assert obj.ping(6000) == 2
assert obj.ping(6001) == 2

obj = RecentCounter()
assert obj.ping(1) == 1
assert obj.ping(10**9) == 1

obj = RecentCounter()
assert obj.ping(10**9 - 3000) == 1
assert obj.ping(10**9) == 2

obj = RecentCounter()
assert [obj.ping(t) for t in range(1, 6)] == [1, 2, 3, 4, 5]

obj = RecentCounter()
results = [obj.ping(t) for t in range(1, 4002)]
assert results[2999] == 3000
assert results[3000] == 3001
assert results[3001] == 3001
assert results[-1] == 3001
assert all(r == min(t, 3001) for t, r in enumerate(results, start=1))

obj = RecentCounter()
assert [obj.ping(t) for t in range(1, 30002, 10)] == [min(i + 1, 301) for i in range(3001)]

a = RecentCounter()
b = RecentCounter()
assert a.ping(1) == 1
assert a.ping(2) == 2
assert b.ping(5) == 1
assert a.ping(3) == 3
assert b.ping(3006) == 1