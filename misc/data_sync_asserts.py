#!/usr/bin/env python3
"""Sequence asserts for the problems of the data-sync chain.

A design problem is driven by a sequence of calls, so a single-call assert
cannot reach the cases that fail on submit: an entry replaced and queried
again, a tie, a delete followed by the same insert, an eviction that must
touch two structures. This script writes those sequences into the prepare
cache of every problem in graph/chains/data-sync.json, in the flat form the
LeetCode examples use: one object, the calls, an assert per read.

    sol = NumberContainers()  # index moved away and back
    sol.change(1, 10)
    sol.change(1, 20)
    sol.change(1, 10)
    assert sol.find(10) == 1

Every expected value is the cached reference solution's, and every sequence
is also run through a short brute-force model of the statement; the two
must agree or the script stops. A read the statement leaves open (getRandom,
getMaxKey on a tie) is asserted with `in` over the answers the model allows.
All inputs stay inside the constraints.

    .venv/bin/python3 misc/data_sync_asserts.py             # write the cache
    .venv/bin/python3 misc/data_sync_asserts.py --dry 2349  # print one block
    .venv/bin/python3 misc/data_sync_asserts.py --random 40 --ops 60

Run it again and the block is replaced, not appended.
"""

import argparse
import ast
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".prepare_cache"
CHAIN = ROOT / "graph" / "chains" / "data-sync.json"
HEADER = "# sequence asserts for the data-sync chain: misc/data_sync_asserts.py"


class Choice:
    """The answers a read may give when the statement allows several."""

    def __init__(self, options):
        self.options = set(options)


# brute-force models: the statement, written the slow way


class FrequencyTracker:
    def __init__(self):
        self.c = Counter()

    def add(self, n):
        self.c[n] += 1

    def deleteOne(self, n):
        if self.c[n] > 0:
            self.c[n] -= 1

    def hasFrequency(self, f):
        return f in self.c.values()


class NumberContainers:
    def __init__(self):
        self.d = {}

    def change(self, i, n):
        self.d[i] = n

    def find(self, n):
        at = [i for i, v in self.d.items() if v == n]
        return min(at) if at else -1


class EventManager:
    def __init__(self, events):
        self.d = {e: p for e, p in events}

    def updatePriority(self, e, p):
        self.d[e] = p

    def pollHighest(self):
        if not self.d:
            return -1
        e = max(self.d, key=lambda e: (self.d[e], -e))
        del self.d[e]
        return e


class RideSharingSystem:
    def __init__(self):
        self.riders, self.drivers = [], []

    def addRider(self, r):
        self.riders.append(r)

    def addDriver(self, d):
        self.drivers.append(d)

    def matchDriverWithRider(self):
        if not self.riders or not self.drivers:
            return [-1, -1]
        return [self.drivers.pop(0), self.riders.pop(0)]

    def cancelRider(self, r):
        if r in self.riders:
            self.riders.remove(r)


class ExamTracker:
    def __init__(self):
        self.rec = []

    def record(self, t, s):
        self.rec.append((t, s))

    def totalScore(self, a, b):
        return sum(s for t, s in self.rec if a <= t <= b)


class RandomizedSet:
    def __init__(self):
        self.s = set()

    def insert(self, v):
        if v in self.s:
            return False
        self.s.add(v)
        return True

    def remove(self, v):
        if v not in self.s:
            return False
        self.s.remove(v)
        return True

    def getRandom(self):
        return Choice(self.s)


class LRUCache:
    def __init__(self, cap):
        self.cap, self.d = cap, OrderedDict()

    def get(self, k):
        if k not in self.d:
            return -1
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v):
        self.d[k] = v
        self.d.move_to_end(k)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)


class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        self.d = {f: [c, r] for f, c, r in zip(foods, cuisines, ratings)}

    def changeRating(self, f, r):
        self.d[f][1] = r

    def highestRated(self, c):
        return min(
            (f for f in self.d if self.d[f][0] == c), key=lambda f: (-self.d[f][1], f)
        )


class TaskManager:
    def __init__(self, tasks):
        self.d = {t: (u, p) for u, t, p in tasks}

    def add(self, u, t, p):
        self.d[t] = (u, p)

    def edit(self, t, p):
        self.d[t] = (self.d[t][0], p)

    def rmv(self, t):
        del self.d[t]

    def execTop(self):
        if not self.d:
            return -1
        t = max(self.d, key=lambda t: (self.d[t][1], t))
        return self.d.pop(t)[0]


class StockPrice:
    def __init__(self):
        self.d = {}

    def update(self, t, p):
        self.d[t] = p

    def current(self):
        return self.d[max(self.d)]

    def maximum(self):
        return max(self.d.values())

    def minimum(self):
        return min(self.d.values())


class Router:
    def __init__(self, limit):
        self.limit, self.q = limit, []

    def addPacket(self, s, d, t):
        if (s, d, t) in self.q:
            return False
        if len(self.q) == self.limit:
            self.q.pop(0)
        self.q.append((s, d, t))
        return True

    def forwardPacket(self):
        return list(self.q.pop(0)) if self.q else []

    def getCount(self, d, a, b):
        return sum(1 for _, dd, t in self.q if dd == d and a <= t <= b)


class AuctionSystem:
    def __init__(self):
        self.d = {}

    def addBid(self, u, i, a):
        self.d[(u, i)] = a

    def updateBid(self, u, i, a):
        self.d[(u, i)] = a

    def removeBid(self, u, i):
        del self.d[(u, i)]

    def getHighestBidder(self, i):
        bids = [(a, u) for (u, ii), a in self.d.items() if ii == i]
        return max(bids)[1] if bids else -1


class AllOne:
    def __init__(self):
        self.c = Counter()

    def inc(self, k):
        self.c[k] += 1

    def dec(self, k):
        self.c[k] -= 1
        if self.c[k] == 0:
            del self.c[k]

    def getMaxKey(self):
        if not self.c:
            return ""
        m = max(self.c.values())
        return Choice(k for k in self.c if self.c[k] == m)

    def getMinKey(self):
        if not self.c:
            return ""
        m = min(self.c.values())
        return Choice(k for k in self.c if self.c[k] == m)


class RandomizedCollection:
    def __init__(self):
        self.c = Counter()

    def insert(self, v):
        self.c[v] += 1
        return self.c[v] == 1

    def remove(self, v):
        if self.c[v] == 0:
            return False
        self.c[v] -= 1
        if self.c[v] == 0:
            del self.c[v]
        return True

    def getRandom(self):
        return Choice(self.c)


class LFUCache:
    def __init__(self, cap):
        self.cap, self.d, self.tick = cap, {}, 0

    def _touch(self, k):
        self.tick += 1
        self.d[k][1] += 1
        self.d[k][2] = self.tick

    def get(self, k):
        if k not in self.d:
            return -1
        self._touch(k)
        return self.d[k][0]

    def put(self, k, v):
        if k in self.d:
            self.d[k][0] = v
            self._touch(k)
            return
        if len(self.d) == self.cap:
            del self.d[min(self.d, key=lambda k: (self.d[k][1], self.d[k][2]))]
        self.tick += 1
        self.d[k] = [v, 1, self.tick]


class FreqStack:
    def __init__(self):
        self.st = []

    def push(self, v):
        self.st.append(v)

    def pop(self):
        c = Counter(self.st)
        m = max(c.values())
        for i in range(len(self.st) - 1, -1, -1):
            if c[self.st[i]] == m:
                return self.st.pop(i)


class DinnerPlates:
    def __init__(self, cap):
        self.cap, self.st = cap, []

    def push(self, v):
        for s in self.st:
            if len(s) < self.cap:
                s.append(v)
                return
        self.st.append([v])

    def pop(self):
        for s in reversed(self.st):
            if s:
                return s.pop()
        return -1

    def popAtStack(self, i):
        if i < len(self.st) and self.st[i]:
            return self.st[i].pop()
        return -1


MODELS = {
    "2671": FrequencyTracker,
    "2349": NumberContainers,
    "3885": EventManager,
    "3829": RideSharingSystem,
    "3709": ExamTracker,
    "380": RandomizedSet,
    "146": LRUCache,
    "2353": FoodRatings,
    "3408": TaskManager,
    "2034": StockPrice,
    "3508": Router,
    "3815": AuctionSystem,
    "432": AllOne,
    "381": RandomizedCollection,
    "460": LFUCache,
    "895": FreqStack,
    "1172": DinnerPlates,
}

# hand-picked sequences: (label, constructor args, calls). The label names
# the input, never the technique. Expected values are not written here;
# the reference computes them and the model checks them.

BIG = 10**9
TARGETED = {
    "2671": [
        (
            "delete a number that was never added",
            (),
            [("deleteOne", 5), ("hasFrequency", 1), ("add", 5), ("hasFrequency", 1)],
        ),
        (
            "add, delete to zero, add again",
            (),
            [
                ("add", 2),
                ("deleteOne", 2),
                ("hasFrequency", 1),
                ("add", 2),
                ("hasFrequency", 1),
                ("hasFrequency", 2),
            ],
        ),
        (
            "two numbers share a count and one moves on",
            (),
            [
                ("add", 1),
                ("add", 2),
                ("hasFrequency", 1),
                ("add", 1),
                ("hasFrequency", 1),
                ("hasFrequency", 2),
                ("add", 2),
                ("hasFrequency", 1),
                ("hasFrequency", 2),
            ],
        ),
        (
            "the count a number just left",
            (),
            [
                ("add", 3),
                ("add", 3),
                ("add", 3),
                ("hasFrequency", 3),
                ("deleteOne", 3),
                ("hasFrequency", 3),
                ("hasFrequency", 2),
            ],
        ),
        (
            "deleted more times than added",
            (),
            [
                ("add", 4),
                ("deleteOne", 4),
                ("deleteOne", 4),
                ("hasFrequency", 1),
                ("add", 4),
                ("hasFrequency", 1),
                ("hasFrequency", 2),
            ],
        ),
        (
            "the largest number, asked for count 1 and for itself",
            (),
            [("add", 100000), ("hasFrequency", 1), ("hasFrequency", 100000)],
        ),
        (
            "a count no number has reached",
            (),
            [
                ("add", 1),
                ("add", 1),
                ("hasFrequency", 3),
                ("hasFrequency", 1),
                ("hasFrequency", 2),
            ],
        ),
        (
            "a count held by two numbers, both leave it",
            (),
            [
                ("add", 1),
                ("add", 2),
                ("deleteOne", 1),
                ("hasFrequency", 1),
                ("deleteOne", 2),
                ("hasFrequency", 1),
            ],
        ),
        (
            "one number climbs to five and back down",
            (),
            [
                ("add", 9),
                ("add", 9),
                ("add", 9),
                ("add", 9),
                ("add", 9),
                ("hasFrequency", 5),
                ("hasFrequency", 4),
                ("deleteOne", 9),
                ("hasFrequency", 5),
                ("hasFrequency", 4),
                ("deleteOne", 9),
                ("deleteOne", 9),
                ("deleteOne", 9),
                ("hasFrequency", 1),
                ("deleteOne", 9),
                ("hasFrequency", 1),
            ],
        ),
    ],
    "2349": [
        ("a number never stored", (), [("find", 10)]),
        (
            "the index moved to another number",
            (),
            [("change", 1, 10), ("change", 1, 20), ("find", 10), ("find", 20)],
        ),
        (
            "the index set to the same number twice, then moved",
            (),
            [
                ("change", 1, 10),
                ("change", 1, 10),
                ("change", 1, 20),
                ("find", 10),
                ("find", 20),
            ],
        ),
        (
            "the index moved away and back",
            (),
            [
                ("change", 1, 10),
                ("change", 1, 20),
                ("change", 1, 10),
                ("find", 10),
                ("find", 20),
                ("change", 1, 20),
                ("find", 10),
                ("find", 20),
            ],
        ),
        (
            "the smallest index moves, the next one answers",
            (),
            [
                ("change", 1, 10),
                ("change", 2, 10),
                ("change", 3, 10),
                ("change", 1, 20),
                ("find", 10),
                ("change", 2, 30),
                ("find", 10),
                ("change", 3, 10),
                ("find", 10),
                ("change", 3, 40),
                ("find", 10),
            ],
        ),
        (
            "a smaller index arrives later",
            (),
            [
                ("change", 5, 10),
                ("find", 10),
                ("change", 2, 10),
                ("find", 10),
                ("change", 2, 20),
                ("find", 10),
            ],
        ),
        (
            "every index leaves the number, then one returns",
            (),
            [
                ("change", 1, 10),
                ("change", 2, 10),
                ("change", 1, 20),
                ("change", 2, 20),
                ("find", 10),
                ("change", 2, 10),
                ("find", 10),
            ],
        ),
        (
            "the largest index and number",
            (),
            [("change", BIG, BIG), ("find", BIG), ("change", 1, BIG), ("find", BIG)],
        ),
        (
            "one index flips between two numbers many times",
            (),
            [
                ("change", 3, 1),
                ("change", 3, 2),
                ("change", 3, 1),
                ("change", 3, 2),
                ("change", 3, 1),
                ("find", 1),
                ("find", 2),
                ("change", 4, 2),
                ("change", 3, 2),
                ("find", 2),
                ("find", 1),
            ],
        ),
        (
            "two indices swap numbers",
            (),
            [
                ("change", 1, 10),
                ("change", 2, 20),
                ("change", 1, 20),
                ("change", 2, 10),
                ("find", 10),
                ("find", 20),
            ],
        ),
    ],
    "3885": [
        (
            "two events tie, the smaller id goes first",
            ([[5, 7], [2, 7], [9, 4]],),
            [("pollHighest",), ("pollHighest",), ("pollHighest",), ("pollHighest",)],
        ),
        (
            "updated to the priority it already has, then polled twice",
            ([[1, 3], [2, 1]],),
            [
                ("updatePriority", 1, 3),
                ("pollHighest",),
                ("pollHighest",),
                ("pollHighest",),
            ],
        ),
        (
            "lowered, then raised back to the old value",
            ([[1, 5], [2, 4]],),
            [
                ("updatePriority", 1, 1),
                ("pollHighest",),
                ("updatePriority", 1, 5),
                ("pollHighest",),
                ("pollHighest",),
            ],
        ),
        (
            "lowered below the other, polled, then the other",
            ([[1, 5], [2, 4]],),
            [("updatePriority", 1, 3), ("pollHighest",), ("pollHighest",)],
        ),
        (
            "raised to tie with a smaller id",
            ([[1, 5], [2, 3]],),
            [("updatePriority", 2, 5), ("pollHighest",), ("pollHighest",)],
        ),
        (
            "raised to tie with a larger id",
            ([[2, 5], [1, 3]],),
            [("updatePriority", 1, 5), ("pollHighest",), ("pollHighest",)],
        ),
        (
            "updated several times before any poll",
            ([[1, 1], [2, 2]],),
            [
                ("updatePriority", 1, 5),
                ("updatePriority", 1, 2),
                ("updatePriority", 1, 9),
                ("updatePriority", 2, 9),
                ("pollHighest",),
                ("pollHighest",),
                ("pollHighest",),
            ],
        ),
        (
            "polled empty twice",
            ([[1, 1]],),
            [("pollHighest",), ("pollHighest",), ("pollHighest",)],
        ),
        (
            "the polled event's old priority is above everything left",
            ([[1, 9], [2, 1]],),
            [
                ("pollHighest",),
                ("updatePriority", 2, 3),
                ("pollHighest",),
                ("pollHighest",),
            ],
        ),
        (
            "the largest id and priority",
            ([[BIG, BIG], [1, BIG]],),
            [("pollHighest",), ("pollHighest",)],
        ),
        (
            "one event updated up and down around another",
            ([[1, 5], [2, 5], [3, 5]],),
            [
                ("updatePriority", 3, 6),
                ("updatePriority", 3, 4),
                ("updatePriority", 3, 6),
                ("updatePriority", 3, 5),
                ("pollHighest",),
                ("pollHighest",),
                ("pollHighest",),
                ("pollHighest",),
            ],
        ),
    ],
    "3829": [
        (
            "a rider with no driver",
            (),
            [
                ("addRider", 1),
                ("matchDriverWithRider",),
                ("addDriver", 2),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "a driver with no rider",
            (),
            [
                ("addDriver", 2),
                ("matchDriverWithRider",),
                ("addRider", 1),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "the first rider cancels, the second is matched",
            (),
            [
                ("addRider", 3),
                ("addRider", 1),
                ("addDriver", 2),
                ("cancelRider", 3),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "cancel a rider never added",
            (),
            [
                ("cancelRider", 7),
                ("addRider", 1),
                ("addDriver", 2),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "cancel a rider already matched",
            (),
            [
                ("addRider", 1),
                ("addDriver", 2),
                ("matchDriverWithRider",),
                ("cancelRider", 1),
                ("addDriver", 3),
                ("addRider", 4),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "cancel the same rider twice",
            (),
            [
                ("addRider", 1),
                ("addRider", 2),
                ("cancelRider", 1),
                ("cancelRider", 1),
                ("addDriver", 5),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "drivers queue up before the riders",
            (),
            [
                ("addDriver", 1),
                ("addDriver", 2),
                ("addDriver", 3),
                ("addRider", 9),
                ("addRider", 8),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
                ("addRider", 7),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "the middle rider cancels",
            (),
            [
                ("addRider", 1),
                ("addRider", 2),
                ("addRider", 3),
                ("cancelRider", 2),
                ("addDriver", 10),
                ("addDriver", 11),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "the last rider cancels",
            (),
            [
                ("addRider", 1),
                ("addRider", 2),
                ("cancelRider", 2),
                ("addDriver", 4),
                ("matchDriverWithRider",),
                ("matchDriverWithRider",),
            ],
        ),
        (
            "the largest ids",
            (),
            [("addRider", 1000), ("addDriver", 1000), ("matchDriverWithRider",)],
        ),
        (
            "every rider cancels",
            (),
            [
                ("addRider", 1),
                ("addRider", 2),
                ("addDriver", 3),
                ("cancelRider", 1),
                ("cancelRider", 2),
                ("matchDriverWithRider",),
                ("addRider", 4),
                ("matchDriverWithRider",),
            ],
        ),
    ],
    "3709": [
        (
            "one record, asked for its own time",
            (),
            [("record", 1, 98), ("totalScore", 1, 1)],
        ),
        (
            "a range before the first record",
            (),
            [
                ("record", 5, 10),
                ("record", 8, 20),
                ("totalScore", 5, 5),
                ("totalScore", 6, 7),
                ("totalScore", 6, 8),
                ("totalScore", 1, 4),
            ],
        ),
        (
            "ranges ending exactly on a record",
            (),
            [
                ("record", 2, 1),
                ("record", 4, 2),
                ("record", 6, 3),
                ("totalScore", 2, 4),
                ("totalScore", 3, 4),
                ("totalScore", 4, 6),
                ("totalScore", 1, 6),
                ("totalScore", 5, 6),
            ],
        ),
        (
            "a range between two records",
            (),
            [
                ("record", 10, 5),
                ("record", 20, 6),
                ("totalScore", 11, 19),
                ("totalScore", 10, 19),
                ("totalScore", 11, 20),
                ("totalScore", 10, 20),
            ],
        ),
        (
            "reads between records",
            (),
            [
                ("record", 1, 1),
                ("totalScore", 1, 1),
                ("record", 3, 2),
                ("totalScore", 1, 3),
                ("totalScore", 2, 3),
                ("record", 4, 4),
                ("totalScore", 1, 4),
                ("totalScore", 4, 4),
                ("totalScore", 2, 2),
            ],
        ),
        (
            "the largest scores",
            (),
            [
                ("record", 1, BIG),
                ("record", 2, BIG),
                ("record", 3, BIG),
                ("totalScore", 1, 3),
                ("totalScore", 2, 2),
            ],
        ),
        (
            "the largest times",
            (),
            [
                ("record", BIG - 1, 5),
                ("record", BIG, 7),
                ("totalScore", 1, BIG),
                ("totalScore", BIG, BIG),
                ("totalScore", 1, BIG - 1),
            ],
        ),
        (
            "records far apart, a range covering only the last",
            (),
            [
                ("record", 1, 1),
                ("record", 100, 2),
                ("record", 10000, 3),
                ("totalScore", 101, 10000),
                ("totalScore", 2, 9999),
                ("totalScore", 1, 100),
            ],
        ),
    ],
    "380": [
        (
            "the same value twice",
            (),
            [("insert", 1), ("insert", 1), ("remove", 1), ("remove", 1)],
        ),
        (
            "remove one of two, the other is the only answer",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("remove", 1),
                ("getRandom",),
                ("insert", 1),
                ("remove", 2),
                ("getRandom",),
            ],
        ),
        (
            "remove the last inserted values",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 3),
                ("remove", 3),
                ("remove", 2),
                ("getRandom",),
            ],
        ),
        (
            "remove the first inserted value",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 3),
                ("remove", 1),
                ("remove", 3),
                ("getRandom",),
                ("remove", 2),
                ("insert", 2),
                ("getRandom",),
            ],
        ),
        (
            "remove the middle value then insert it again",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 3),
                ("remove", 2),
                ("insert", 2),
                ("remove", 1),
                ("remove", 2),
                ("getRandom",),
            ],
        ),
        (
            "negative and extreme values",
            (),
            [
                ("insert", -2147483648),
                ("insert", 2147483647),
                ("remove", -2147483648),
                ("getRandom",),
                ("remove", 2147483647),
                ("insert", 0),
                ("getRandom",),
            ],
        ),
        (
            "remove everything, then insert again",
            (),
            [
                ("insert", 5),
                ("remove", 5),
                ("insert", 5),
                ("getRandom",),
                ("remove", 5),
                ("remove", 5),
                ("insert", 6),
                ("getRandom",),
            ],
        ),
        (
            "random over two values, then over one",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("getRandom",),
                ("remove", 1),
                ("getRandom",),
            ],
        ),
        (
            "remove in insertion order",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 3),
                ("insert", 4),
                ("remove", 1),
                ("remove", 2),
                ("remove", 3),
                ("getRandom",),
                ("insert", 1),
                ("remove", 4),
                ("getRandom",),
            ],
        ),
    ],
    "146": [
        (
            "the official example",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 1),
                ("put", 3, 3),
                ("get", 2),
                ("put", 4, 4),
                ("get", 1),
                ("get", 3),
                ("get", 4),
            ],
        ),
        (
            "put on a key already present",
            (2,),
            [
                ("put", 2, 1),
                ("put", 1, 1),
                ("put", 2, 3),
                ("put", 4, 1),
                ("get", 1),
                ("get", 2),
                ("get", 4),
            ],
        ),
        (
            "a read keeps a key alive",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 1),
                ("put", 3, 3),
                ("get", 2),
                ("get", 1),
                ("get", 3),
            ],
        ),
        (
            "a read of a missing key changes nothing",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 3),
                ("put", 3, 3),
                ("get", 1),
                ("get", 2),
            ],
        ),
        (
            "capacity 1",
            (1,),
            [
                ("put", 1, 1),
                ("get", 1),
                ("put", 2, 2),
                ("get", 1),
                ("get", 2),
                ("put", 2, 5),
                ("get", 2),
                ("get", 1),
            ],
        ),
        (
            "overwriting does not evict",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("put", 1, 9),
                ("get", 2),
                ("get", 1),
                ("put", 3, 3),
                ("get", 2),
                ("get", 1),
                ("get", 3),
            ],
        ),
        (
            "key 0 and value 0",
            (2,),
            [
                ("put", 0, 0),
                ("get", 0),
                ("put", 1, 0),
                ("get", 1),
                ("put", 2, 2),
                ("get", 0),
                ("get", 1),
                ("get", 2),
            ],
        ),
        (
            "reads reorder three keys before two evictions",
            (3,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("put", 3, 3),
                ("get", 1),
                ("get", 2),
                ("put", 4, 4),
                ("get", 3),
                ("get", 1),
                ("put", 5, 5),
                ("get", 2),
                ("get", 4),
                ("get", 5),
            ],
        ),
        (
            "the same key put over and over",
            (2,),
            [
                ("put", 1, 1),
                ("put", 1, 2),
                ("put", 1, 3),
                ("put", 2, 2),
                ("put", 1, 4),
                ("put", 3, 3),
                ("get", 2),
                ("get", 1),
                ("get", 3),
            ],
        ),
        (
            "the largest key and value",
            (2,),
            [
                ("put", 10000, 100000),
                ("get", 10000),
                ("put", 0, 0),
                ("put", 1, 1),
                ("get", 10000),
            ],
        ),
    ],
    "2353": [
        (
            "the official example",
            (
                ["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
                ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
                [9, 12, 8, 15, 14, 7],
            ),
            [
                ("highestRated", "korean"),
                ("highestRated", "japanese"),
                ("changeRating", "sushi", 16),
                ("highestRated", "japanese"),
                ("changeRating", "ramen", 16),
                ("highestRated", "japanese"),
            ],
        ),
        (
            "two foods tie",
            (["b", "a"], ["x", "x"], [5, 5]),
            [
                ("highestRated", "x"),
                ("changeRating", "a", 4),
                ("highestRated", "x"),
                ("changeRating", "b", 4),
                ("highestRated", "x"),
            ],
        ),
        (
            "lowered, then raised back",
            (["a", "b"], ["x", "x"], [5, 3]),
            [
                ("changeRating", "a", 1),
                ("highestRated", "x"),
                ("changeRating", "a", 5),
                ("highestRated", "x"),
                ("changeRating", "a", 3),
                ("highestRated", "x"),
            ],
        ),
        (
            "changed to the rating it already has",
            (["a", "b"], ["x", "x"], [5, 3]),
            [
                ("changeRating", "a", 5),
                ("highestRated", "x"),
                ("changeRating", "b", 5),
                ("highestRated", "x"),
                ("changeRating", "a", 4),
                ("highestRated", "x"),
            ],
        ),
        (
            "a cuisine with one food",
            (["a", "b"], ["x", "y"], [1, 9]),
            [
                ("highestRated", "x"),
                ("changeRating", "a", 1),
                ("highestRated", "x"),
                ("highestRated", "y"),
                ("changeRating", "b", 2),
                ("highestRated", "y"),
            ],
        ),
        (
            "several changes before a read",
            (["a", "b", "c"], ["x", "x", "x"], [1, 2, 3]),
            [
                ("changeRating", "a", 9),
                ("changeRating", "b", 9),
                ("changeRating", "c", 9),
                ("highestRated", "x"),
                ("changeRating", "a", 8),
                ("highestRated", "x"),
                ("changeRating", "b", 1),
                ("highestRated", "x"),
                ("changeRating", "c", 2),
                ("highestRated", "x"),
            ],
        ),
        (
            "raised past the top, then lowered under everyone",
            (["a", "b", "c"], ["x", "x", "x"], [3, 2, 1]),
            [
                ("changeRating", "c", 10),
                ("highestRated", "x"),
                ("changeRating", "c", 1),
                ("highestRated", "x"),
                ("changeRating", "a", 1),
                ("highestRated", "x"),
                ("changeRating", "b", 1),
                ("highestRated", "x"),
            ],
        ),
        (
            "ratings at the limit",
            (["a", "b"], ["x", "x"], [10**8, 10**8 - 1]),
            [
                ("highestRated", "x"),
                ("changeRating", "b", 10**8),
                ("highestRated", "x"),
                ("changeRating", "a", 1),
                ("highestRated", "x"),
            ],
        ),
        (
            "longer names that share a prefix",
            (["abc", "ab", "abcd"], ["x", "x", "x"], [2, 2, 2]),
            [
                ("highestRated", "x"),
                ("changeRating", "ab", 1),
                ("highestRated", "x"),
                ("changeRating", "abc", 1),
                ("highestRated", "x"),
            ],
        ),
    ],
    "3408": [
        (
            "the official example",
            ([[1, 101, 10], [2, 102, 20], [3, 103, 15]],),
            [
                ("add", 4, 104, 5),
                ("edit", 102, 8),
                ("execTop",),
                ("rmv", 101),
                ("add", 5, 105, 15),
                ("execTop",),
            ],
        ),
        (
            "a tie on priority, the larger taskId first",
            ([[1, 101, 5], [2, 102, 5]],),
            [("execTop",), ("execTop",), ("execTop",)],
        ),
        (
            "edited to the priority it already has, then executed twice",
            ([[1, 101, 5], [2, 102, 1]],),
            [("edit", 101, 5), ("execTop",), ("execTop",), ("execTop",)],
        ),
        (
            "edited down, then back up",
            ([[1, 101, 5], [2, 102, 4]],),
            [
                ("edit", 101, 1),
                ("execTop",),
                ("edit", 101, 5),
                ("execTop",),
                ("execTop",),
            ],
        ),
        (
            "the top task removed",
            ([[1, 101, 9], [2, 102, 1]],),
            [("rmv", 101), ("execTop",), ("execTop",)],
        ),
        (
            "everything removed, then one added",
            ([[1, 101, 9]],),
            [
                ("rmv", 101),
                ("execTop",),
                ("add", 3, 103, 1),
                ("execTop",),
                ("execTop",),
            ],
        ),
        (
            "edited up to a tie with a larger taskId",
            ([[1, 101, 5], [2, 100, 3]],),
            [("edit", 100, 5), ("execTop",), ("execTop",)],
        ),
        (
            "one user with several tasks",
            ([[7, 1, 1], [7, 2, 2], [7, 3, 3]],),
            [("execTop",), ("rmv", 2), ("execTop",), ("execTop",)],
        ),
        (
            "priority 0, taskId 0, userId 0",
            ([[0, 0, 0]],),
            [("execTop",), ("execTop",)],
        ),
        (
            "a task edited, then removed",
            ([[1, 101, 1], [2, 102, 2]],),
            [("edit", 101, 9), ("rmv", 101), ("execTop",), ("execTop",)],
        ),
        (
            "an edit after another task was removed",
            ([[1, 101, 1], [2, 102, 2], [3, 103, 3]],),
            [("rmv", 103), ("edit", 101, 3), ("execTop",), ("execTop",), ("execTop",)],
        ),
        (
            "added after every initial task is gone",
            ([[1, 1, 1]],),
            [
                ("execTop",),
                ("add", 2, 2, 2),
                ("add", 3, 3, 2),
                ("execTop",),
                ("execTop",),
                ("execTop",),
            ],
        ),
        (
            "the largest values",
            ([[100000, 100000, BIG], [0, 99999, BIG]],),
            [("execTop",), ("execTop",)],
        ),
    ],
    "2034": [
        (
            "the official example",
            (),
            [
                ("update", 1, 10),
                ("update", 2, 5),
                ("current",),
                ("maximum",),
                ("update", 1, 3),
                ("maximum",),
                ("update", 4, 2),
                ("minimum",),
            ],
        ),
        (
            "the latest timestamp corrected",
            (),
            [
                ("update", 1, 10),
                ("update", 1, 3),
                ("current",),
                ("maximum",),
                ("minimum",),
            ],
        ),
        (
            "an earlier timestamp arrives after a later one",
            (),
            [
                ("update", 5, 10),
                ("update", 2, 99),
                ("current",),
                ("maximum",),
                ("update", 2, 1),
                ("maximum",),
                ("minimum",),
                ("current",),
            ],
        ),
        (
            "the maximum corrected down, then up again",
            (),
            [
                ("update", 1, 10),
                ("update", 2, 5),
                ("update", 1, 1),
                ("maximum",),
                ("update", 1, 10),
                ("maximum",),
                ("update", 1, 1),
                ("maximum",),
                ("minimum",),
            ],
        ),
        (
            "the minimum corrected up",
            (),
            [
                ("update", 1, 1),
                ("update", 2, 9),
                ("minimum",),
                ("update", 1, 9),
                ("minimum",),
                ("maximum",),
                ("update", 2, 2),
                ("minimum",),
            ],
        ),
        (
            "the same price at two timestamps, one corrected",
            (),
            [
                ("update", 1, 5),
                ("update", 2, 5),
                ("update", 1, 1),
                ("maximum",),
                ("minimum",),
                ("update", 2, 1),
                ("maximum",),
            ],
        ),
        (
            "one update, every read",
            (),
            [("update", 3, 7), ("current",), ("maximum",), ("minimum",)],
        ),
        (
            "the largest timestamp and price",
            (),
            [
                ("update", BIG, BIG),
                ("update", 1, 1),
                ("current",),
                ("maximum",),
                ("minimum",),
                ("update", BIG, 1),
                ("current",),
                ("maximum",),
            ],
        ),
        (
            "the same timestamp corrected many times",
            (),
            [
                ("update", 1, 5),
                ("update", 1, 6),
                ("update", 1, 4),
                ("update", 1, 8),
                ("update", 1, 2),
                ("maximum",),
                ("minimum",),
                ("current",),
            ],
        ),
        (
            "the old maximum and minimum both corrected away",
            (),
            [
                ("update", 1, 1),
                ("update", 2, 9),
                ("update", 3, 5),
                ("update", 1, 5),
                ("update", 2, 5),
                ("maximum",),
                ("minimum",),
                ("current",),
            ],
        ),
    ],
    "3508": [
        (
            "the official example",
            (3,),
            [
                ("addPacket", 1, 4, 90),
                ("addPacket", 2, 5, 90),
                ("addPacket", 1, 4, 90),
                ("addPacket", 3, 5, 95),
                ("addPacket", 4, 5, 105),
                ("forwardPacket",),
                ("addPacket", 5, 2, 110),
                ("getCount", 5, 100, 110),
            ],
        ),
        (
            "the same packet after it was forwarded",
            (2,),
            [
                ("addPacket", 1, 2, 3),
                ("forwardPacket",),
                ("addPacket", 1, 2, 3),
                ("forwardPacket",),
                ("forwardPacket",),
            ],
        ),
        (
            "the same packet after it was pushed out",
            (2,),
            [
                ("addPacket", 1, 2, 5),
                ("addPacket", 1, 3, 5),
                ("addPacket", 1, 4, 5),
                ("addPacket", 1, 2, 5),
                ("getCount", 2, 5, 5),
                ("getCount", 3, 5, 5),
                ("forwardPacket",),
                ("forwardPacket",),
                ("forwardPacket",),
            ],
        ),
        (
            "a packet pushed out lowers its destination's count",
            (2,),
            [
                ("addPacket", 1, 9, 1),
                ("addPacket", 2, 9, 2),
                ("getCount", 9, 1, 2),
                ("addPacket", 3, 9, 3),
                ("getCount", 9, 1, 2),
                ("getCount", 9, 1, 3),
                ("forwardPacket",),
                ("getCount", 9, 1, 3),
            ],
        ),
        (
            "forward on empty",
            (2,),
            [
                ("forwardPacket",),
                ("getCount", 1, 1, 1),
                ("addPacket", 1, 1, 1),
                ("forwardPacket",),
                ("forwardPacket",),
                ("getCount", 1, 1, 1),
            ],
        ),
        (
            "a range holding no packet",
            (3,),
            [
                ("addPacket", 1, 1, 10),
                ("addPacket", 1, 1, 20),
                ("getCount", 1, 11, 19),
                ("getCount", 1, 10, 10),
                ("getCount", 1, 20, 20),
                ("getCount", 1, 1, 100),
                ("getCount", 2, 1, 100),
            ],
        ),
        (
            "equal timestamps from different sources",
            (3,),
            [
                ("addPacket", 1, 1, 5),
                ("addPacket", 2, 1, 5),
                ("addPacket", 1, 1, 5),
                ("getCount", 1, 5, 5),
                ("forwardPacket",),
                ("getCount", 1, 5, 5),
                ("addPacket", 1, 1, 5),
                ("getCount", 1, 5, 5),
                ("forwardPacket",),
                ("forwardPacket",),
            ],
        ),
        (
            "a duplicate while full does not push anything out",
            (2,),
            [
                ("addPacket", 1, 1, 1),
                ("addPacket", 2, 1, 1),
                ("addPacket", 1, 1, 1),
                ("getCount", 1, 1, 1),
                ("forwardPacket",),
                ("forwardPacket",),
            ],
        ),
        (
            "the largest values",
            (2,),
            [
                ("addPacket", 200000, 200000, BIG),
                ("getCount", 200000, 1, BIG),
                ("forwardPacket",),
                ("getCount", 200000, 1, BIG),
            ],
        ),
        (
            "packets to two destinations pushed out in turn",
            (3,),
            [
                ("addPacket", 1, 1, 1),
                ("addPacket", 1, 2, 2),
                ("addPacket", 1, 1, 3),
                ("addPacket", 1, 2, 4),
                ("getCount", 1, 1, 4),
                ("getCount", 2, 1, 4),
                ("addPacket", 1, 1, 5),
                ("getCount", 2, 1, 5),
                ("forwardPacket",),
                ("getCount", 1, 1, 5),
                ("forwardPacket",),
                ("getCount", 2, 1, 5),
            ],
        ),
    ],
    "3815": [
        (
            "a tie goes to the larger userId",
            (),
            [
                ("addBid", 1, 1, 5),
                ("addBid", 2, 1, 5),
                ("getHighestBidder", 1),
                ("addBid", 3, 1, 5),
                ("getHighestBidder", 1),
                ("removeBid", 3, 1),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "addBid replaces the user's bid",
            (),
            [
                ("addBid", 1, 1, 9),
                ("addBid", 2, 1, 5),
                ("addBid", 1, 1, 1),
                ("getHighestBidder", 1),
                ("addBid", 1, 1, 6),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "updated down, then back up, then to a tie",
            (),
            [
                ("addBid", 1, 1, 9),
                ("addBid", 2, 1, 5),
                ("updateBid", 1, 1, 1),
                ("getHighestBidder", 1),
                ("updateBid", 1, 1, 9),
                ("getHighestBidder", 1),
                ("updateBid", 1, 1, 5),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "the highest removed, then the next",
            (),
            [
                ("addBid", 1, 1, 3),
                ("addBid", 2, 1, 2),
                ("addBid", 3, 1, 1),
                ("removeBid", 1, 1),
                ("getHighestBidder", 1),
                ("removeBid", 2, 1),
                ("getHighestBidder", 1),
                ("removeBid", 3, 1),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "an item nobody bid on",
            (),
            [
                ("getHighestBidder", 5),
                ("addBid", 1, 5, 1),
                ("getHighestBidder", 5),
                ("getHighestBidder", 6),
            ],
        ),
        (
            "removed, then bid again",
            (),
            [
                ("addBid", 1, 1, 5),
                ("removeBid", 1, 1),
                ("getHighestBidder", 1),
                ("addBid", 1, 1, 2),
                ("getHighestBidder", 1),
                ("addBid", 2, 1, 3),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "one user on two items",
            (),
            [
                ("addBid", 1, 1, 5),
                ("addBid", 1, 2, 1),
                ("addBid", 2, 2, 2),
                ("getHighestBidder", 1),
                ("getHighestBidder", 2),
                ("updateBid", 1, 2, 2),
                ("getHighestBidder", 2),
                ("updateBid", 1, 2, 3),
                ("getHighestBidder", 2),
                ("removeBid", 1, 1),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "updated to the amount it already has",
            (),
            [
                ("addBid", 1, 1, 5),
                ("addBid", 2, 1, 4),
                ("updateBid", 1, 1, 5),
                ("getHighestBidder", 1),
                ("removeBid", 1, 1),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "the removed user's old amount is above the rest",
            (),
            [
                ("addBid", 3, 1, 9),
                ("addBid", 1, 1, 1),
                ("removeBid", 3, 1),
                ("getHighestBidder", 1),
                ("addBid", 3, 1, 1),
                ("getHighestBidder", 1),
            ],
        ),
        (
            "the largest ids and amounts",
            (),
            [
                ("addBid", 50000, 50000, BIG),
                ("addBid", 1, 50000, BIG),
                ("getHighestBidder", 50000),
                ("removeBid", 50000, 50000),
                ("getHighestBidder", 50000),
            ],
        ),
    ],
    "432": [
        (
            "the official example",
            (),
            [
                ("inc", "hello"),
                ("inc", "hello"),
                ("getMaxKey",),
                ("getMinKey",),
                ("inc", "leet"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "empty, then one key, then empty again",
            (),
            [
                ("getMaxKey",),
                ("getMinKey",),
                ("inc", "a"),
                ("getMaxKey",),
                ("dec", "a"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "a key counted down to zero",
            (),
            [
                ("inc", "a"),
                ("inc", "b"),
                ("inc", "b"),
                ("dec", "a"),
                ("getMaxKey",),
                ("getMinKey",),
                ("inc", "a"),
                ("getMinKey",),
            ],
        ),
        (
            "two keys tie, then part",
            (),
            [
                ("inc", "a"),
                ("inc", "b"),
                ("getMaxKey",),
                ("getMinKey",),
                ("inc", "a"),
                ("getMaxKey",),
                ("getMinKey",),
                ("inc", "b"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "a key climbs past another",
            (),
            [
                ("inc", "a"),
                ("inc", "a"),
                ("inc", "b"),
                ("getMinKey",),
                ("inc", "b"),
                ("inc", "b"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "the top key counted down step by step",
            (),
            [
                ("inc", "a"),
                ("inc", "a"),
                ("inc", "a"),
                ("inc", "b"),
                ("dec", "a"),
                ("getMaxKey",),
                ("dec", "a"),
                ("getMaxKey",),
                ("dec", "a"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "the middle count empties",
            (),
            [
                ("inc", "a"),
                ("inc", "b"),
                ("inc", "b"),
                ("inc", "c"),
                ("inc", "c"),
                ("inc", "c"),
                ("dec", "b"),
                ("getMinKey",),
                ("getMaxKey",),
                ("dec", "c"),
                ("dec", "c"),
                ("getMaxKey",),
                ("getMinKey",),
            ],
        ),
        (
            "the longest keys",
            (),
            [
                ("inc", "abcdefghij"),
                ("inc", "abcdefghij"),
                ("inc", "a"),
                ("getMaxKey",),
                ("getMinKey",),
                ("dec", "abcdefghij"),
                ("dec", "abcdefghij"),
                ("getMaxKey",),
            ],
        ),
        (
            "the only key counted up and down",
            (),
            [
                ("inc", "z"),
                ("inc", "z"),
                ("inc", "z"),
                ("dec", "z"),
                ("dec", "z"),
                ("getMaxKey",),
                ("getMinKey",),
                ("dec", "z"),
                ("getMaxKey",),
                ("inc", "z"),
                ("getMinKey",),
            ],
        ),
    ],
    "381": [
        (
            "the official example",
            (),
            [
                ("insert", 1),
                ("insert", 1),
                ("insert", 2),
                ("getRandom",),
                ("remove", 1),
                ("getRandom",),
            ],
        ),
        (
            "the only copy removed, then the duplicates",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 2),
                ("remove", 1),
                ("getRandom",),
                ("remove", 2),
                ("getRandom",),
                ("remove", 2),
                ("remove", 2),
            ],
        ),
        (
            "the removed value is also the last inserted",
            (),
            [
                ("insert", 1),
                ("insert", 1),
                ("insert", 2),
                ("insert", 1),
                ("remove", 1),
                ("remove", 1),
                ("remove", 1),
                ("getRandom",),
                ("remove", 1),
            ],
        ),
        (
            "copies spread through the sequence, all removed",
            (),
            [
                ("insert", 4),
                ("insert", 3),
                ("insert", 4),
                ("insert", 2),
                ("insert", 4),
                ("remove", 4),
                ("remove", 4),
                ("remove", 4),
                ("remove", 4),
                ("remove", 3),
                ("getRandom",),
            ],
        ),
        (
            "insert says whether the value was absent",
            (),
            [
                ("insert", 1),
                ("remove", 1),
                ("insert", 1),
                ("insert", 1),
                ("remove", 1),
                ("insert", 1),
                ("remove", 1),
                ("remove", 1),
                ("insert", 1),
            ],
        ),
        (
            "negative and extreme values",
            (),
            [
                ("insert", -2147483648),
                ("insert", 2147483647),
                ("insert", -2147483648),
                ("remove", 2147483647),
                ("getRandom",),
                ("remove", -2147483648),
                ("getRandom",),
            ],
        ),
        (
            "remove a missing value",
            (),
            [
                ("remove", 5),
                ("insert", 5),
                ("remove", 6),
                ("getRandom",),
                ("remove", 5),
                ("remove", 5),
            ],
        ),
        (
            "interleaved removals leave one value",
            (),
            [
                ("insert", 1),
                ("insert", 2),
                ("insert", 3),
                ("insert", 2),
                ("insert", 1),
                ("remove", 2),
                ("remove", 1),
                ("remove", 3),
                ("remove", 2),
                ("getRandom",),
            ],
        ),
        (
            "remove the first copy while the last copy sits at the end",
            (),
            [
                ("insert", 7),
                ("insert", 8),
                ("insert", 7),
                ("remove", 7),
                ("remove", 8),
                ("getRandom",),
                ("remove", 7),
                ("remove", 7),
                ("insert", 9),
                ("getRandom",),
            ],
        ),
    ],
    "460": [
        (
            "the official example",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 1),
                ("put", 3, 3),
                ("get", 2),
                ("get", 3),
                ("put", 4, 4),
                ("get", 1),
                ("get", 3),
                ("get", 4),
            ],
        ),
        (
            "a tie on use count, the least recently used goes",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 1),
                ("get", 2),
                ("put", 3, 3),
                ("get", 1),
                ("get", 2),
                ("get", 3),
            ],
        ),
        (
            "put on a key already present counts as a use",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("put", 1, 5),
                ("put", 3, 3),
                ("get", 2),
                ("get", 1),
                ("get", 3),
            ],
        ),
        (
            "reads of a missing key count for nothing",
            (2,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 3),
                ("get", 3),
                ("get", 3),
                ("put", 3, 3),
                ("get", 1),
                ("get", 2),
                ("get", 3),
            ],
        ),
        (
            "capacity 1",
            (1,),
            [
                ("put", 1, 1),
                ("get", 1),
                ("put", 2, 2),
                ("get", 1),
                ("get", 2),
                ("put", 2, 9),
                ("get", 2),
            ],
        ),
        (
            "a newcomer starts below every old key",
            (2,),
            [
                ("put", 1, 1),
                ("get", 1),
                ("get", 1),
                ("put", 2, 2),
                ("put", 3, 3),
                ("get", 2),
                ("get", 1),
                ("get", 3),
                ("put", 4, 4),
                ("get", 3),
                ("get", 4),
                ("get", 1),
            ],
        ),
        (
            "every key used once more, then two newcomers",
            (3,),
            [
                ("put", 1, 1),
                ("put", 2, 2),
                ("put", 3, 3),
                ("get", 1),
                ("get", 2),
                ("get", 3),
                ("put", 4, 4),
                ("get", 1),
                ("put", 5, 5),
                ("get", 4),
                ("get", 5),
                ("get", 2),
                ("get", 3),
            ],
        ),
        (
            "key 0 and value 0",
            (2,),
            [
                ("put", 0, 0),
                ("get", 0),
                ("put", 1, 1),
                ("put", 2, 2),
                ("get", 1),
                ("get", 0),
                ("get", 2),
            ],
        ),
        (
            "an evicted key put again starts from one",
            (2,),
            [
                ("put", 1, 1),
                ("get", 1),
                ("get", 1),
                ("put", 2, 2),
                ("put", 3, 3),
                ("put", 2, 2),
                ("get", 3),
                ("get", 2),
                ("get", 1),
            ],
        ),
        (
            "the largest key and value",
            (2,),
            [
                ("put", 100000, BIG),
                ("get", 100000),
                ("put", 0, 0),
                ("put", 1, 1),
                ("get", 100000),
                ("get", 0),
            ],
        ),
    ],
    "895": [
        (
            "the official example",
            (),
            [
                ("push", 5),
                ("push", 7),
                ("push", 5),
                ("push", 7),
                ("push", 4),
                ("push", 5),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "a tie resolved by the most recent",
            (),
            [
                ("push", 1),
                ("push", 2),
                ("push", 1),
                ("push", 2),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "pop, then push the same value again",
            (),
            [
                ("push", 1),
                ("push", 1),
                ("push", 2),
                ("pop",),
                ("push", 2),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "one value pushed four times over another",
            (),
            [
                ("push", 3),
                ("push", 3),
                ("push", 3),
                ("push", 3),
                ("push", 1),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "value 0 and the largest value",
            (),
            [("push", 0), ("push", BIG), ("push", 0), ("pop",), ("pop",), ("pop",)],
        ),
        (
            "all values distinct",
            (),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "a count falls, then rises again",
            (),
            [
                ("push", 1),
                ("push", 1),
                ("push", 2),
                ("push", 2),
                ("push", 2),
                ("pop",),
                ("pop",),
                ("pop",),
                ("push", 2),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "the stack emptied and refilled",
            (),
            [
                ("push", 1),
                ("push", 2),
                ("pop",),
                ("pop",),
                ("push", 2),
                ("push", 1),
                ("push", 1),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
    ],
    "1172": [
        (
            "the official example",
            (2,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("push", 5),
                ("popAtStack", 0),
                ("push", 20),
                ("push", 21),
                ("popAtStack", 0),
                ("popAtStack", 2),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "pop on empty, and a stack that was never made",
            (2,),
            [
                ("pop",),
                ("popAtStack", 0),
                ("push", 1),
                ("popAtStack", 5),
                ("pop",),
                ("pop",),
                ("popAtStack", 0),
            ],
        ),
        (
            "capacity 1",
            (1,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("popAtStack", 1),
                ("push", 4),
                ("popAtStack", 1),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "pushes fill the leftmost gap first",
            (2,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("push", 5),
                ("push", 6),
                ("popAtStack", 0),
                ("popAtStack", 0),
                ("popAtStack", 0),
                ("push", 7),
                ("push", 8),
                ("push", 9),
                ("pop",),
                ("pop",),
                ("popAtStack", 0),
                ("pop",),
            ],
        ),
        (
            "pop passes over empty stacks on the right",
            (2,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("popAtStack", 1),
                ("popAtStack", 1),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "the rightmost stack emptied by index, then pop",
            (1,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("popAtStack", 2),
                ("popAtStack", 2),
                ("pop",),
                ("push", 5),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "several gaps, then pushes",
            (2,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("push", 5),
                ("push", 6),
                ("push", 7),
                ("push", 8),
                ("popAtStack", 2),
                ("popAtStack", 0),
                ("popAtStack", 1),
                ("push", 9),
                ("push", 10),
                ("push", 11),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
            ],
        ),
        (
            "an index far beyond every stack",
            (3,),
            [
                ("popAtStack", 100000),
                ("push", 1),
                ("popAtStack", 100000),
                ("popAtStack", 0),
                ("popAtStack", 0),
            ],
        ),
        (
            "a gap on the left stays while pops come from the right",
            (2,),
            [
                ("push", 1),
                ("push", 2),
                ("push", 3),
                ("push", 4),
                ("popAtStack", 0),
                ("pop",),
                ("pop",),
                ("pop",),
                ("pop",),
                ("push", 5),
                ("pop",),
            ],
        ),
    ],
}


# random sequences: valid calls with a small value space, so entries
# collide, tie, get replaced and get deleted


def rand_2671(rng, n):
    ops = []
    for _ in range(n):
        k = rng.random()
        if k < 0.45:
            ops.append(("add", rng.randint(1, 4)))
        elif k < 0.7:
            ops.append(("deleteOne", rng.randint(1, 4)))
        else:
            ops.append(("hasFrequency", rng.randint(1, 4)))
    return (), ops


def rand_2349(rng, n):
    ops = []
    for _ in range(n):
        if rng.random() < 0.6:
            ops.append(("change", rng.randint(1, 5), rng.choice([10, 20, 30])))
        else:
            ops.append(("find", rng.choice([10, 20, 30, 40])))
    return (), ops


def rand_3885(rng, n):
    ids = rng.sample(range(1, 10), rng.randint(2, 6))
    events = [[e, rng.randint(1, 4)] for e in ids]
    m, ops = EventManager(events), []
    for _ in range(n):
        if m.d and rng.random() < 0.55:
            e, p = rng.choice(sorted(m.d)), rng.randint(1, 4)
            m.updatePriority(e, p)
            ops.append(("updatePriority", e, p))
        else:
            was_empty = not m.d
            m.pollHighest()
            ops.append(("pollHighest",))
            if was_empty:
                break
    return (events,), ops


def rand_3829(rng, n):
    riders, drivers, ops = list(range(1, 13)), list(range(1, 13)), []
    rng.shuffle(riders)
    rng.shuffle(drivers)
    for _ in range(n):
        k = rng.random()
        if k < 0.3 and riders:
            ops.append(("addRider", riders.pop()))
        elif k < 0.55 and drivers:
            ops.append(("addDriver", drivers.pop()))
        elif k < 0.75:
            ops.append(("cancelRider", rng.randint(1, 12)))
        else:
            ops.append(("matchDriverWithRider",))
    return (), ops


def rand_3709(rng, n):
    t, ops = 0, []
    for i in range(n):
        if i == 0 or rng.random() < 0.5:
            t += rng.randint(1, 3)
            ops.append(("record", t, rng.randint(1, 9)))
        else:
            a = rng.randint(1, t)
            ops.append(("totalScore", a, rng.randint(a, t)))
    return (), ops


def rand_380(rng, n):
    m, ops = RandomizedSet(), []
    for _ in range(n):
        k = rng.random()
        if k < 0.4:
            v = rng.randint(-2, 3)
            m.insert(v)
            ops.append(("insert", v))
        elif k < 0.75:
            v = rng.randint(-2, 3)
            m.remove(v)
            ops.append(("remove", v))
        elif m.s:
            ops.append(("getRandom",))
    return (), ops


def rand_146(rng, n):
    ops = []
    for _ in range(n):
        if rng.random() < 0.55:
            ops.append(("put", rng.randint(0, 4), rng.randint(0, 9)))
        else:
            ops.append(("get", rng.randint(0, 4)))
    return (rng.randint(1, 3),), ops


def rand_2353(rng, n):
    names = ["a", "b", "c", "ab", "ba", "d"]
    foods = rng.sample(names, rng.randint(2, 6))
    cuisines = [rng.choice(["x", "y"]) for _ in foods]
    ratings = [rng.randint(1, 5) for _ in foods]
    ops = []
    for _ in range(n):
        if rng.random() < 0.5:
            ops.append(("changeRating", rng.choice(foods), rng.randint(1, 5)))
        else:
            ops.append(("highestRated", rng.choice(cuisines)))
    return (foods, cuisines, ratings), ops


def rand_3408(rng, n):
    fresh = list(range(20))
    rng.shuffle(fresh)
    tasks = [
        [rng.randint(0, 3), fresh.pop(), rng.randint(0, 4)]
        for _ in range(rng.randint(1, 4))
    ]
    m, ops = TaskManager(tasks), []
    for _ in range(n):
        k = rng.random()
        if k < 0.3 and fresh:
            u, t, p = rng.randint(0, 3), fresh.pop(), rng.randint(0, 4)
            m.add(u, t, p)
            ops.append(("add", u, t, p))
        elif k < 0.5 and m.d:
            t, p = rng.choice(sorted(m.d)), rng.randint(0, 4)
            m.edit(t, p)
            ops.append(("edit", t, p))
        elif k < 0.65 and m.d:
            t = rng.choice(sorted(m.d))
            m.rmv(t)
            ops.append(("rmv", t))
        else:
            m.execTop()
            ops.append(("execTop",))
    return (tasks,), ops


def rand_2034(rng, n):
    ops = [("update", rng.randint(1, 6), rng.randint(1, 9))]
    for _ in range(n - 1):
        k = rng.random()
        if k < 0.5:
            ops.append(("update", rng.randint(1, 6), rng.randint(1, 9)))
        else:
            ops.append((rng.choice(["current", "maximum", "minimum"]),))
    return (), ops


def rand_3508(rng, n):
    t, ops = 1, []
    for _ in range(n):
        k = rng.random()
        if k < 0.5:
            t += rng.randint(0, 2)
            ops.append(("addPacket", rng.randint(1, 3), rng.randint(1, 3), t))
        elif k < 0.75:
            ops.append(("forwardPacket",))
        else:
            a = rng.randint(1, t + 1)
            ops.append(("getCount", rng.randint(1, 3), a, rng.randint(a, t + 1)))
    return (rng.randint(2, 4),), ops


def rand_3815(rng, n):
    m, ops = AuctionSystem(), []
    for _ in range(n):
        k = rng.random()
        if k < 0.35:
            u, i, a = rng.randint(1, 4), rng.randint(1, 2), rng.randint(1, 5)
            m.addBid(u, i, a)
            ops.append(("addBid", u, i, a))
        elif k < 0.5 and m.d:
            (u, i), a = rng.choice(sorted(m.d)), rng.randint(1, 5)
            m.updateBid(u, i, a)
            ops.append(("updateBid", u, i, a))
        elif k < 0.65 and m.d:
            u, i = rng.choice(sorted(m.d))
            m.removeBid(u, i)
            ops.append(("removeBid", u, i))
        else:
            ops.append(("getHighestBidder", rng.randint(1, 2)))
    return (), ops


def rand_432(rng, n):
    m, ops = AllOne(), []
    for _ in range(n):
        k = rng.random()
        if k < 0.4:
            key = rng.choice("abcd")
            m.inc(key)
            ops.append(("inc", key))
        elif k < 0.65 and m.c:
            key = rng.choice(sorted(m.c))
            m.dec(key)
            ops.append(("dec", key))
        else:
            ops.append((rng.choice(["getMaxKey", "getMinKey"]),))
    return (), ops


def rand_381(rng, n):
    m, ops = RandomizedCollection(), []
    for _ in range(n):
        k = rng.random()
        if k < 0.45:
            v = rng.randint(-1, 2)
            m.insert(v)
            ops.append(("insert", v))
        elif k < 0.8:
            v = rng.randint(-1, 2)
            m.remove(v)
            ops.append(("remove", v))
        elif m.c:
            ops.append(("getRandom",))
    return (), ops


def rand_895(rng, n):
    size, ops = 0, []
    for _ in range(n):
        if size == 0 or rng.random() < 0.55:
            size += 1
            ops.append(("push", rng.randint(1, 3)))
        else:
            size -= 1
            ops.append(("pop",))
    return (), ops


def rand_1172(rng, n):
    ops = []
    for _ in range(n):
        k = rng.random()
        if k < 0.5:
            ops.append(("push", rng.randint(1, 9)))
        elif k < 0.7:
            ops.append(("pop",))
        else:
            ops.append(("popAtStack", rng.randint(0, 4)))
    return (rng.randint(1, 3),), ops


RANDOM = {
    "2671": rand_2671,
    "2349": rand_2349,
    "3885": rand_3885,
    "3829": rand_3829,
    "3709": rand_3709,
    "380": rand_380,
    "146": rand_146,
    "2353": rand_2353,
    "3408": rand_3408,
    "2034": rand_2034,
    "3508": rand_3508,
    "3815": rand_3815,
    "432": rand_432,
    "381": rand_381,
    "460": rand_146,
    "895": rand_895,
    "1172": rand_1172,
}


# running and writing


def reference(num, name):
    """The class `name` from the cached reference solution of problem num."""
    src = json.loads((CACHE / f"{num}.json").read_text())["solution"]
    keep = [
        n
        for n in ast.parse(src).body
        if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.Import, ast.ImportFrom))
    ]
    ns = {}
    exec(compile(ast.Module(keep, type_ignores=[]), f"<{num}>", "exec"), ns)
    return ns[name]


def run(cls, ctor, ops):
    obj = cls(*ctor)
    return [getattr(obj, m)(*args) for m, *args in ops]


def expected(num, cls, ctor, ops):
    """The reference's answer to every call, checked against the model. A
    read the model leaves open comes back as a Choice."""
    got = run(cls, ctor, ops)
    want = run(MODELS[num], ctor, ops)
    out = []
    for (m, *args), g, w in zip(ops, got, want):
        if isinstance(w, Choice):
            if g not in w.options:
                sys.exit(
                    f"{num}: {m}{tuple(args)} gave {g!r}, the statement allows {w.options}"
                )
            out.append(w if len(w.options) > 1 else next(iter(w.options)))
        else:
            if g != w:
                sys.exit(
                    f"{num}: {m}{tuple(args)} gave {g!r}, the statement says {w!r}"
                )
            out.append(g)
    return out


def lit(v):
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(lit(x) for x in v) + "]"
    if isinstance(v, Choice):
        return "{" + ", ".join(lit(x) for x in sorted(v.options)) + "}"
    raise TypeError(repr(v))


def lines(name, label, ctor, ops, results):
    out = [f"sol = {name}({', '.join(lit(a) for a in ctor)})  # {label}"]
    for (m, *args), r in zip(ops, results):
        call = f"sol.{m}({', '.join(lit(a) for a in args)})"
        if r is None:
            out.append(call)
        elif isinstance(r, Choice):
            out.append(f"assert {call} in {lit(r)}")
        elif isinstance(r, bool):
            out.append(f"assert {call} is {lit(r)}")
        else:
            out.append(f"assert {call} == {lit(r)}")
    return out


def block(num, name, cls, n_random, n_ops, seed):
    rng = random.Random(seed * 100003 + int(num))
    parts = [
        HEADER,
        "# the values are the reference solution's; a read the statement leaves"
        "\n# open is asserted over every answer it allows",
    ]
    for label, ctor, ops in TARGETED[num]:
        parts.append(
            "\n".join(lines(name, label, ctor, ops, expected(num, cls, ctor, ops)))
        )
    for i in range(n_random):
        ctor, ops = RANDOM[num](rng, n_ops)
        label = f"random sequence {i + 1}"
        parts.append(
            "\n".join(lines(name, label, ctor, ops, expected(num, cls, ctor, ops)))
        )
    return "\n\n".join(parts) + "\n"


def merged(text, new):
    """text with the block replaced, or appended under two blank lines."""
    at = text.find(HEADER)
    base = text[:at].rstrip("\n") if at >= 0 else text.rstrip("\n")
    return f"{base}\n\n\n{new}"


def black(text):
    done = subprocess.run(
        [str(ROOT / ".venv" / "bin" / "black"), "-q", "-"],
        input=text,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return done.stdout if done.returncode == 0 else text


def validate(text):
    with tempfile.NamedTemporaryFile("w", suffix=".py", dir=CACHE, delete=False) as f:
        f.write(text)
    try:
        done = subprocess.run(
            [str(ROOT / ".venv" / "bin" / "python3"), f.name],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=120,
        )
    finally:
        Path(f.name).unlink()
    return done.returncode == 0, done.stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("nums", nargs="*", help="problem numbers; default: the whole chain")
    ap.add_argument(
        "--dry", action="store_true", help="print the blocks, write nothing"
    )
    ap.add_argument(
        "--random", type=int, default=20, help="random sequences per problem"
    )
    ap.add_argument("--ops", type=int, default=30, help="calls per random sequence")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    chain = json.loads(CHAIN.read_text())
    nums = a.nums or chain["order"]
    for num in nums:
        path = CACHE / f"{num}.json"
        raw = path.read_text()
        d = json.loads(raw)
        name = next(
            n.name for n in ast.parse(d["solution"]).body if isinstance(n, ast.ClassDef)
        )
        cls = reference(num, name)
        text = block(num, name, cls, a.random, a.ops, a.seed)
        if a.dry:
            print(text)
            continue
        solution = black(merged(d["solution"], text))
        ok, err = validate(solution)
        if not ok:
            sys.exit(f"{num}: the merged solution fails\n{err}")
        d["solution"] = solution
        d["code"] = black(merged(d["code"], text))
        path.write_text(
            json.dumps(d, ensure_ascii=raw.isascii())
            + ("\n" if raw.endswith("\n") else "")
        )
        print(
            f"{num}. {d['title']}: {text.count(chr(10))} lines, {text.count('assert ')} asserts"
        )


if __name__ == "__main__":
    main()
