"""
DRILL: Reorder A Late Feed
TRAINS: late-event-buffer

Score updates arrive from a provider with a timestamp, out of order by at
most L seconds: an update with timestamp t arrives before every update
whose timestamp is greater than t + L. Emit the updates in timestamp
order, ties in arrival order. Solution(L) has

    push(ts, value) -> list of (ts, value) released, in timestamp order
    flush() -> list of (ts, value) still held, in timestamp order
    dropped() -> int

The watermark is the largest timestamp pushed so far minus L. After a
push, every held update whose timestamp is below the watermark is
released, smallest first. An update that arrives with a timestamp already
below the watermark is late: it is dropped, counted, and nothing is
released. flush releases everything still held and empties the buffer.

Example 1:

    feed = Solution(2)
    feed.push(1, "a")   -> []
    feed.push(4, "b")   -> [(1, "a")]              (watermark 2)
    feed.push(3, "c")   -> []
    feed.push(2, "d")   -> []                      (2 is not below 2: held)
    feed.push(6, "e")   -> [(2, "d"), (3, "c")]    (watermark 4)
    feed.push(1, "f")   -> []                      (1 is below 4: dropped)
    feed.flush()        -> [(4, "b"), (6, "e")]
    feed.dropped()      -> 1

Constraints:

    0 <= ts <= 10^9
    0 <= L <= 10^9
    up to 10^6 pushes

    REQUIRED: O(log n) per push, n held. NO sort of the buffer on a push.
"""


class Solution:
    def __init__(self, lateness: int):
        pass

    def push(self, ts: int, value: str) -> list:
        pass

    def flush(self) -> list:
        pass

    def dropped(self) -> int:
        pass


feed = Solution(2)

feed.push(1, "a")
print(feed.push(4, "b"))  # [(1, 'a')]

# assert feed.push(3, "c") == []
# assert feed.push(2, "d") == []
# assert feed.push(6, "e") == [(2, "d"), (3, "c")]
# assert feed.push(1, "f") == []
# assert feed.dropped() == 1
# assert feed.flush() == [(4, "b"), (6, "e")]
# assert feed.flush() == []
# assert feed.dropped() == 1
# feed2 = Solution(0)
# assert feed2.push(5, "x") == []
# assert feed2.push(5, "y") == []
# assert feed2.push(7, "z") == [(5, "x"), (5, "y")]
# assert feed2.push(6, "w") == []
# assert feed2.dropped() == 1
# assert feed2.flush() == [(7, "z")]
# feed3 = Solution(10)
# assert feed3.push(10, "p") == []
# assert feed3.push(3, "q") == []
# assert feed3.push(13, "r") == []
# assert feed3.push(20, "s") == [(3, "q")]
# assert feed3.push(11, "t") == []
# assert feed3.push(30, "u") == [(10, "p"), (11, "t"), (13, "r")]
# assert feed3.flush() == [(20, "s"), (30, "u")]
# assert feed3.dropped() == 0
