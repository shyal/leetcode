"""
Sliding window over a sequence.

The window is the half-open span [left, right] of self.seq. It carries a
summary of its own contents, kept correct by exactly two O(1) edits: add
when an element enters on the right, remove when one leaves on the left.
Nothing in here ever recomputes the summary from the span.

`valid` is the invariant, and it is the only thing that decides which end
moves. The five loops below are the whole family:

    slide_fixed       width pinned at k
    longest           shrink WHILE INVALID, then measure
    longest_no_shrink same answer, width never decreases, left moves at
                      most once per step, and the final width IS the answer
    shortest          measure WHILE VALID, then shrink
    count_windows     shrink while invalid, then add right - left + 1

`longest` and `longest_no_shrink` return the same number. Only a minimum
window and a count need the inner while loop; a maximum never does, since
a briefly illegal window is harmless when a wider legal one was already
seen. Carrying the no-shrink shape into a minimum-window problem is the
classic way to get answers that are too large.

When the invariant is "the window covers a target multiset", do not
compare two tallies. Keep one integer counting how many characters sit at
the amount the target asks for, and move it only when a count crosses that
amount. That makes `valid` O(1) instead of O(len(target)).

Boundary: a max or min over the window cannot be maintained this way.
Removing the largest element leaves no way to name the new largest without
looking at the span again. That case needs a monotonic deque, which is the
deque-recent-window node, not this one.
"""


class Window:
    def __init__(self, seq):
        self.seq = seq
        self.left = 0
        self.counts = defaultdict(int)
        self.distinct = 0

    def add(self, x):
        self.counts[x] += 1
        if self.counts[x] == 1:
            self.distinct += 1

    def remove(self, x):
        self.counts[x] -= 1
        if self.counts[x] == 0:
            self.distinct -= 1

    def valid(self):
        return True

    def slide_fixed(self, k, report):
        best = None
        for right in range(len(self.seq)):
            self.add(self.seq[right])
            if right >= k:
                self.remove(self.seq[right - k])
                self.left = right - k + 1
            if right >= k - 1:
                seen = report(self)
                best = seen if best is None else max(best, seen)
        return best

    def longest(self):
        best = 0
        self.left = 0
        for right in range(len(self.seq)):
            self.add(self.seq[right])
            while not self.valid():
                self.remove(self.seq[self.left])
                self.left += 1
            best = max(best, right - self.left + 1)
        return best

    def longest_no_shrink(self):
        self.left = 0
        for right in range(len(self.seq)):
            self.add(self.seq[right])
            if not self.valid():
                self.remove(self.seq[self.left])
                self.left += 1
        return len(self.seq) - self.left

    def shortest(self):
        best = 0
        self.left = 0
        for right in range(len(self.seq)):
            self.add(self.seq[right])
            while self.valid():
                width = right - self.left + 1
                best = width if best == 0 else min(best, width)
                self.remove(self.seq[self.left])
                self.left += 1
        return best

    def count_windows(self):
        total = 0
        self.left = 0
        for right in range(len(self.seq)):
            self.add(self.seq[right])
            while not self.valid():
                self.remove(self.seq[self.left])
                self.left += 1
            total += right - self.left + 1
        return total


if __name__ == "__main__":

    class AtMost(Window):
        def __init__(self, seq, k):
            super().__init__(seq)
            self.k = k

        def valid(self):
            return self.distinct <= self.k

    class AtLeast(Window):
        def __init__(self, seq, k):
            super().__init__(seq)
            self.k = k

        def valid(self):
            return self.distinct >= self.k

    # widest span holding at most k different characters
    assert AtMost("eceba", 2).longest() == 3
    assert AtMost("aabbcc", 2).longest() == 4

    # the no-shrink loop returns the same widths without ever narrowing
    assert AtMost("eceba", 2).longest_no_shrink() == 3
    assert AtMost("aabbcc", 2).longest_no_shrink() == 4
    assert AtMost("abcabcabc", 3).longest_no_shrink() == 9

    # narrowest span holding at least k different characters
    assert AtLeast("abcabc", 3).shortest() == 3
    assert AtLeast("aaab", 2).shortest() == 2
    assert AtLeast("aaa", 2).shortest() == 0

    # how many spans hold at most k different characters
    assert AtMost("abca", 2).count_windows() == 7
    assert AtMost("aaa", 1).count_windows() == 6

    # exactly k is the difference of two at-most counts
    assert AtMost("abca", 2).count_windows() - AtMost("abca", 1).count_windows() == 3

    # widest count of different characters across a pinned width
    assert Window("abcba").slide_fixed(3, lambda w: w.distinct) == 3
    assert Window("aaaa").slide_fixed(2, lambda w: w.distinct) == 1

    print("All tests passed!")
