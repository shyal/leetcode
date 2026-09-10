from operator import lt, gt


class Type:
    decreasing = 0
    increasing = 1


class MonotonicQueue:

    def __init__(self, type: Type = Type.increasing):
        self.queue = deque([])
        self.type = type

    def push(self, val):
        op = (lt, gt)[self.type]
        res = []
        while self.queue and op(self.queue[-1][0], val[0]):
            res.append(self.queue.pop())
        self.queue.append(val)
        return res

    def pop(self):
        if self.queue:
            return self.queue.pop()

    def popleft(self):
        if self.queue:
            return self.queue.popleft()

    def peek(self):
        if self.queue:
            return self.queue[-1]

    def front(self):
        if self.queue:
            return self.queue[0]

    def __str__(self):
        return str(self.queue)


queue = MonotonicQueue(Type.decreasing)
vals = [5, 4, 3, 2, 1, 3]
res = []
for i, v in enumerate(vals):
    r = queue.push((v, i))
    res.extend(r)
assert res == [(1, 4), (2, 3)]  # these two got evicted by the last 3
assert list(queue.queue) == [(5, 0), (4, 1), (3, 2), (3, 5)]
assert queue.front() == (5, 0)  # the largest is always at the front
queue.popleft()
assert queue.front() == (4, 1)
