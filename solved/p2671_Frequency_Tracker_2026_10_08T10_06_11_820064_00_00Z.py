# combo chain: data-sync, problem 1 of 17. Run `make combos data-sync` to see
# the chain and what is done this lap; the chain is saved in graph/chains/data-sync.json.
"""
URL: https://leetcode.com/problems/frequency-tracker/description/?envType=problem-list-v2&envId=vn57k9wr

2671. Frequency Tracker

Design a data structure that keeps track of the values in it and answers some queries regarding their frequencies.

Implement the FrequencyTracker class.

- FrequencyTracker(): Initializes the FrequencyTracker object with an empty array initially.
- void add(int number): Adds number to the data structure.
- void deleteOne(int number): Deletes one occurrence of number from the data structure. The data structure may not contain number, and in this case nothing is deleted.
- bool hasFrequency(int frequency): Returns true if there is a number in the data structure that occurs frequency number of times, otherwise, it returns false.

Example 1:

Input
["FrequencyTracker", "add", "add", "hasFrequency"]
[[], [3], [3], [2]]
Output
[null, null, null, true]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(3); // The data structure now contains [3]
frequencyTracker.add(3); // The data structure now contains [3, 3]
frequencyTracker.hasFrequency(2); // Returns true, because 3 occurs twice

Example 2:

Input
["FrequencyTracker", "add", "deleteOne", "hasFrequency"]
[[], [1], [1], [1]]
Output
[null, null, null, false]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(1); // The data structure now contains [1]
frequencyTracker.deleteOne(1); // The data structure becomes empty []
frequencyTracker.hasFrequency(1); // Returns false, because the data structure is empty

Example 3:

Input
["FrequencyTracker", "hasFrequency", "add", "hasFrequency"]
[[], [2], [3], [1]]
Output
[null, false, null, true]

Explanation
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.hasFrequency(2); // Returns false, because the data structure is empty
frequencyTracker.add(3); // The data structure now contains [3]
frequencyTracker.hasFrequency(1); // Returns true, because 3 occurs once

Constraints:

    1 <= number <= 10^5
    1 <= frequency <= 10^5
    At most, 2 * 10^5 calls will be made to add, deleteOne, and hasFrequency in total.

---

LEETCODE: Accepted (118 ms, 74.5 MB)
"""


class FrequencyTracker:

    def __init__(self):
        self.d = defaultdict(int)
        self.f = defaultdict(int)

    def add(self, number: int) -> None:
        if self.d[number] in self.f:
            self.f[self.d[number]] -= 1
            if self.f[self.d[number]] == 0:
                del self.f[self.d[number]]
        self.d[number] += 1
        self.f[self.d[number]] += 1

    def deleteOne(self, number: int) -> None:
        # this is fast, because dicts use a hashing algorithm
        # thus the key lookup is in O(1) amortized
        if number in self.d:
            if self.d[number] in self.f:
                self.f[self.d[number]] -= 1
            if self.f[self.d[number]] == 0:
                del self.f[self.d[number]]
            self.d[number] -= 1
            if self.d[number] == 0:
                del self.d[number]
            else:
                self.f[self.d[number]] += 1

    def hasFrequency(self, frequency: int) -> bool:
        # this is the slow part
        # because frequency in self.d.values() is in O(N)
        # but we want it to be faster
        # using a heap would cost n log n to pull everything out
        return frequency in self.f


sol = FrequencyTracker()

sol.add(3)
sol.add(3)
print(sol.hasFrequency(2))  # True

sol = FrequencyTracker()
sol.add(1)
sol.deleteOne(1)
print(sol.hasFrequency(1))  # False

sol = FrequencyTracker()
print(sol.hasFrequency(2))  # False
sol.add(3)
print(sol.hasFrequency(1))  # True


assert (
    lambda: (f := FrequencyTracker(), f.add(3), f.add(3), f.hasFrequency(2))[-1]
)() == True
assert (
    lambda: (f := FrequencyTracker(), f.add(1), f.deleteOne(1), f.hasFrequency(1))[-1]
)() == False
assert (
    lambda: (f := FrequencyTracker(), f.hasFrequency(2), f.add(3), f.hasFrequency(1))[
        -1
    ]
)() == True

assert (lambda: (f := FrequencyTracker(), f.hasFrequency(1))[-1])() == False
assert (
    lambda: (f := FrequencyTracker(), f.add(5), f.add(5), f.add(5), f.hasFrequency(3))[
        -1
    ]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(10**5),
        f.add(10**5),
        f.deleteOne(10**5),
        f.hasFrequency(1),
    )[-1]
)() == True
assert (
    lambda: (f := FrequencyTracker(), f.deleteOne(1), f.hasFrequency(1))[-1]
)() == False
assert (
    lambda: (
        f := FrequencyTracker(),
        [f.add(i) for i in range(1, 101)],
        f.hasFrequency(1),
    )[-1]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        [f.add(7) for _ in range(1000)],
        f.hasFrequency(1000),
    )[-1]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(4),
        f.deleteOne(4),
        f.deleteOne(4),
        f.hasFrequency(0),
    )[-1]
)() == False
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(1),
        f.add(1),
        f.deleteOne(1),
        f.hasFrequency(1),
    )[-1]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(1),
        f.add(2),
        f.add(2),
        f.deleteOne(2),
        f.hasFrequency(1),
    )[-1]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(1),
        f.add(1),
        f.add(2),
        f.deleteOne(1),
        f.hasFrequency(1),
    )[-1]
)() == True
assert (
    lambda: (
        f := FrequencyTracker(),
        f.add(10**5),
        f.deleteOne(10**5),
        f.hasFrequency(1),
    )[-1]
)() == False
