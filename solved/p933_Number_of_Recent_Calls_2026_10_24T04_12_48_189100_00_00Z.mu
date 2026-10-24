# URL: https://leetcode.com/problems/number-of-recent-calls/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 933. Number of Recent Calls
#
# You have a RecentCounter class which counts the number of recent requests within a certain time frame.
#
# Implement the RecentCounter class:
#
# - RecentCounter() Initializes the counter with zero recent requests.
# - int ping(int t) Adds a new request at time t, where t represents some time in milliseconds, and returns the number of requests that has happened in the past 3000 milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range [t - 3000, t].
#
# It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.
#
# Example 1:
#
# Input
# ["RecentCounter","ping","ping","ping","ping"]
# [[],[1],[100],[3001],[3002]]
# Output
# [null,1,2,3,3]
#
# Explanation:
# RecentCounter recentCounter = new RecentCounter();
# recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
# recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
# recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
# recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3
#
# Constraints:
#
#     1 <= t <= 10^9
#     Each test case will call ping with strictly increasing values of t.
#     At most 10^4 calls will be made to ping.
#
# ---
# LEETCODE: Accepted (108 ms, 24.1 MB)

# mu 0.12

class RecentCounter
  def __init__()
    self.d = deque([])

  def ping(t: int) -> int
    self.d <- t
    while self.d and self.d[0] < t - 3000
      self.d.popleft()
    len self.d


sol = RecentCounter()

print(sol.ping(1))  # 1

assert sol.ping(100) == 2
assert sol.ping(3001) == 3
assert sol.ping(3002) == 3
assert RecentCounter().ping(1) == 1

# t - 3000 is inside the range: the request at 1 counts for the ping at 3001
edge = RecentCounter()
assert edge.ping(1) == 1
assert edge.ping(3001) == 2
assert edge.ping(3002) == 2

# a gap longer than 3000 removes all old requests
gap = RecentCounter()
assert gap.ping(1) == 1
assert gap.ping(2) == 2
assert gap.ping(10000) == 1
assert gap.ping(13001) == 1

# requests in the same range all count
dense = RecentCounter()
for i in range(1, 101)
  assert dense.ping(i) == i
assert dense.ping(3001) == 101
assert dense.ping(3002) == 101

# the largest t
assert RecentCounter().ping(10**9) == 1
