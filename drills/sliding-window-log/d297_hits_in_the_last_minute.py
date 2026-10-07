"""
DRILL: Hits In The Last Minute
TRAINS: sliding-window-log

Count each user's requests over a sliding window. Solution(window) has

    hit(user, now) -> int

hit records a request by user at time now and returns the number of that
user's requests in the window, this one included: the requests whose
time is greater than now - window. The time now is an int in seconds
and never decreases.

Example 1:

    log = Solution(60)
    log.hit("ann", 0)      -> 1
    log.hit("ann", 30)     -> 2
    log.hit("ann", 60)     -> 2     (the request at 0 is out of the window)
    log.hit("bob", 60)     -> 1
    log.hit("ann", 89)     -> 3
    log.hit("ann", 90)     -> 3     (30 is out, 90 is in)
    log.hit("ann", 1000)   -> 1

Constraints:

    1 <= window <= 10^6
    0 <= now <= 10^9
    up to 10^6 calls

    REQUIRED: O(1) amortised per call, and the memory per user is that
    user's requests inside the window: nothing older is kept. NO scan of
    every request to count.
"""


class Solution:
    def __init__(self, window: int):
        pass

    def hit(self, user: str, now: int) -> int:
        pass


log = Solution(60)

log.hit("ann", 0)
log.hit("ann", 30)
print(log.hit("ann", 60))  # 2

# assert log.hit("bob", 60) == 1
# assert log.hit("ann", 89) == 3
# assert log.hit("ann", 90) == 3
# assert log.hit("ann", 1000) == 1
# assert log.hit("bob", 1000) == 1
# log2 = Solution(1)
# assert log2.hit("c", 5) == 1
# assert log2.hit("c", 5) == 2
# assert log2.hit("c", 6) == 1
# assert log2.hit("c", 7) == 1
# log3 = Solution(10)
# assert all(log3.hit("d", t) == min(t + 1, 10) for t in range(100))
