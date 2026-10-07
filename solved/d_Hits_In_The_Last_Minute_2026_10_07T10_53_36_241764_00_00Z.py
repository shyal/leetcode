# combo chain: backend-live-coding, problem 2 of 12. Run `make combos backend-live-coding` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend-live-coding.json.
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


# mu 0.7
# def __init__(window: int)
#   self.d = deque([])
#   self.count = {}
#   self.window = window
#
# def hit(user: str, now: int) -> int
#   self.d <- [user, now]
#   if user not in self.count
#     self.count[user] = 0
#   self.count[user] += 1
#   while self.d and self.d[0][1] <= now - self.window
#     u, t = self.d.popleft()
#     self.count[u] -= 1
#   ret = self.count[user]
#   ret

class Solution:
    def __init__(self, window: int):
        self.d = deque([])
        self.count = {}
        self.window = window

    def hit(self, user: str, now: int) -> int:
        self.d.append([user, now])
        if user not in self.count:
            self.count[user] = 0
        self.count[user] += 1
        while self.d and self.d[0][1] <= now - self.window:
            u, t = self.d.popleft()
            self.count[u] -= 1
        ret = self.count[user]
        return ret


log = Solution(60)
log.hit('ann', 0)
log.hit('ann', 30)
print(log.hit('ann', 60))
_l, _r = log.hit('bob', 60), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log.hit('ann', 89), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log.hit('ann', 90), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log.hit('ann', 1000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log.hit('bob', 1000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
log2 = Solution(1)
_l, _r = log2.hit('c', 5), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log2.hit('c', 5), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log2.hit('c', 6), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = log2.hit('c', 7), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
log3 = Solution(10)
assert all((log3.hit('d', t) == min(t + 1, 10) for t in range(0, 100)))
