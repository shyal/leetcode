"""
DRILL: Cache With Expiry
TRAINS: ttl-cache

Implement a cache whose entries expire. Solution() has

    set(key, value, ttl, now)
    get(key, now) -> value or None
    expire(now) -> int
    size() -> int

An entry set at time now with ttl expires at now + ttl: from that time
on it is gone. set on a key that exists replaces its value and its
expiry. get returns None for a missing or expired key, and removes an
expired key it finds. expire removes every expired entry and returns how
many it removed. size is the number of entries held, expired or not. The
time now is an int and never decreases.

Example 1:

    sol = Solution()
    sol.set("a", 1, 5, 0)
    sol.get("a", 4)     -> 1
    sol.get("a", 5)     -> None    (expired at 5, removed)
    sol.set("b", 2, 10, 0)
    sol.set("c", 3, 3, 0)
    sol.set("c", 4, 20, 1)         (c now expires at 21)
    sol.expire(5)       -> 0
    sol.size()          -> 2
    sol.expire(10)      -> 1       (b)
    sol.get("c", 21)    -> None
    sol.size()          -> 0

Constraints:

    up to 10^6 calls

    REQUIRED: expire in O(k log n) for the k entries it removes, n held;
    get and set in O(log n) or better. NO scan of every key.
"""


class Solution:
    def __init__(self):
        pass

    def set(self, key: str, value, ttl: int, now: int) -> None:
        pass

    def get(self, key: str, now: int):
        pass

    def expire(self, now: int) -> int:
        pass

    def size(self) -> int:
        pass


sol = Solution()

sol.set("a", 1, 5, 0)
print(sol.get("a", 4))  # 1

# assert sol.get("a", 5) is None
# assert sol.size() == 0
# sol.set("b", 2, 10, 0)
# sol.set("c", 3, 3, 0)
# sol.set("c", 4, 20, 1)
# assert sol.expire(5) == 0
# assert sol.size() == 2
# assert sol.get("c", 5) == 4
# assert sol.expire(10) == 1
# assert sol.size() == 1
# assert sol.get("b", 10) is None
# assert sol.get("c", 20) == 4
# assert sol.get("c", 21) is None
# assert sol.size() == 0
# sol.set("d", 5, 1, 30)
# sol.set("e", 6, 1, 30)
# sol.set("f", 7, 100, 30)
# assert sol.expire(30) == 0
# assert sol.expire(31) == 2
# assert sol.size() == 1
# sol.set("f", 8, 1, 31)
# assert sol.expire(32) == 1
# assert sol.size() == 0
# assert sol.expire(1000) == 0
