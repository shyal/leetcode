"""
DRILL: Counts In and Out
TRAINS: sliding-window-fixed

A cloakroom holds coats. Every coat has a colour. Coats arrive one at a
time and leave one at a time.

Given those arrivals and departures, keep two facts correct at every
moment: how many coats of each colour the cloakroom holds, and how many
different colours it holds.

Write `add` and `remove`. The counts live in `self.counts` and the number
of different colours lives in `self.distinct`. Both are set up for you.

Example 1:

Input: add("red"), add("blue"), add("red")
Output: counts["red"] == 2, counts["blue"] == 1, distinct == 2

Example 2:

Input: then remove("red")
Output: counts["red"] == 1, distinct == 2
Explanation: one red coat is still held, so red still counts as a colour.

Example 3:

Input: then remove("red")
Output: counts["red"] == 0, distinct == 1
Explanation: the last red coat left, so red stops counting as a colour.

Constraints:

    add and remove are each called up to 10^5 times.
    remove is never called for a colour the cloakroom does not hold.

    REQUIRED: O(1) per call, touching one colour. `distinct` is
    MAINTAINED, never recounted. Walking counts to recount it, with
    len([c for c in counts if counts[c]]) or anything of that shape, is
    the failure mode this drill exists to kill. A colour starts counting
    when its count rises from 0 to 1 and stops when it falls from 1 to 0.
"""


class Solution:
    def __init__(self) -> None:
        self.counts = defaultdict(int)
        self.distinct = 0

    def add(self, colour: str) -> None:
        if colour not in self.counts:
            self.distinct += 1
        self.counts[colour] += 1

    def remove(self, colour: str) -> None:
        if colour in self.counts:
            if self.counts[colour] == 1:
                self.distinct -= 1
                del self.counts[colour]
            else:
                self.counts[colour] -= 1


sol = Solution()

sol.add("red")
assert sol.counts["red"] == 1 and sol.distinct == 1

sol.add("blue")
assert sol.counts["blue"] == 1 and sol.distinct == 2

sol.add("red")
assert sol.counts["red"] == 2 and sol.distinct == 2

sol.remove("red")
assert sol.counts["red"] == 1 and sol.distinct == 2

sol.remove("red")
assert sol.counts["red"] == 0 and sol.distinct == 1

sol.remove("blue")
assert sol.counts["blue"] == 0 and sol.distinct == 0

sol = Solution()
for c in "aabbcc":
    sol.add(c)
assert sol.distinct == 3
for c in "abc":
    sol.remove(c)
assert sol.distinct == 3
for c in "abc":
    sol.remove(c)
assert sol.distinct == 0

sol = Solution()
sol.add("x")
sol.remove("x")
sol.add("x")
assert sol.counts["x"] == 1 and sol.distinct == 1

print("All tests passed!")
