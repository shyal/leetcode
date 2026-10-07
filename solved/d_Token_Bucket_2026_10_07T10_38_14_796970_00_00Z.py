# combo chain: backend-live-coding, problem 1 of 12. Run `make combos backend-live-coding` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend-live-coding.json.
"""
DRILL: Token Bucket
TRAINS: token-bucket-limit

Rate limit an API per user with a token bucket. Each user's bucket holds
at most capacity tokens and refills at rate tokens per second,
continuously. A request costs one token: when the bucket holds at least
one, take it and allow the request; otherwise refuse it. A user's bucket
is full the first time the user is seen. Solution(capacity, rate) has

    allow(user, now) -> bool

The time now is a float in seconds and never decreases for one user.

Example 1:

    lim = Solution(2, 1.0)
    lim.allow("a", 0.0)   -> True
    lim.allow("a", 0.0)   -> True
    lim.allow("a", 0.0)   -> False
    lim.allow("a", 0.5)   -> False   (0.5 tokens)
    lim.allow("a", 1.0)   -> True    (1.0 token, now 0)
    lim.allow("b", 1.0)   -> True    (another bucket)
    lim.allow("a", 10.0)  -> True    (refilled, capped at 2)
    lim.allow("a", 10.0)  -> True
    lim.allow("a", 10.0)  -> False

Constraints:

    1 <= capacity <= 10^6
    0 < rate <= 10^6
    up to 10^6 calls

    REQUIRED: O(1) per call and O(1) state per user. NO timer and NO pass
    over every user to refill.
"""


# mu 0.7
# def __init__(capacity: int, rate: float)
#   self.capacity = capacity
#   self.rate = rate
#   self.tokens = {}
#   self.last = {}
#
#
# def allow(user: str, now: float) -> bool
#   if user not in self.tokens
#     self.tokens[user] = self.capacity
#     self.last[user] = now
#
#   delta = now - self.last[user]
#   refill = delta * self.rate
#   self.tokens[user] = min(self.capacity, self.tokens[user] + refill)
#   self.last[user] = now
#   if self.tokens[user] >= 1
#     self.tokens[user] -= 1
#     return True
#   return False
#

class Solution:
    def __init__(self, capacity: int, rate: float):
        self.capacity = capacity
        self.rate = rate
        self.tokens = {}
        self.last = {}

    def allow(self, user: str, now: float) -> bool:
        if user not in self.tokens:
            self.tokens[user] = self.capacity
            self.last[user] = now
        delta = now - self.last[user]
        refill = delta * self.rate
        self.tokens[user] = min(self.capacity, self.tokens[user] + refill)
        self.last[user] = now
        if self.tokens[user] >= 1:
            self.tokens[user] -= 1
            return True
        return False


lim = Solution(2, 1.0)
lim.allow('a', 0.0)
lim.allow('a', 0.0)
print(lim.allow('a', 0.0))
_l, _r = lim.allow('a', 0.5), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = lim.allow('a', 1.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('b', 1.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('a', 1.0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('a', 10.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('a', 10.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('a', 10.0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('b', 1.5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('b', 1.5), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim.allow('b', 2.5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
lim2 = Solution(1, 0.5)
_l, _r = lim2.allow('c', 0.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim2.allow('c', 1.0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim2.allow('c', 2.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim2.allow('c', 3.0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim2.allow('c', 100.0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = lim2.allow('c', 100.0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
