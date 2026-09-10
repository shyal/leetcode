from operator import gt, lt


class Type:
    decreasing = 0
    increasing = 1


class MonotonicStack:

    def __init__(self, type: Type = Type.increasing):
        self.data = []
        self.type = type

    def push(self, val):
        op = (lt, gt)[self.type]
        res = []
        while self.data and op(self.data[-1][0], val[0]):
            res.append(self.data.pop())
        self.data.append(val)
        return res

    def pop(self):
        if self.data:
            return self.data.pop()

    def peek(self):
        if self.data:
            return self.data[-1]

    def __str__(self):
        return str(self.data)


stack = MonotonicStack(Type.decreasing)
vals = [5, 4, 3, 2, 1, 3]
res = []
for i, v in enumerate(vals):
    r = stack.push((v, i))
    res.extend(r)
assert res == [(1, 4), (2, 3)]  # these two got evicted by the last 3
assert stack.data == [(5, 0), (4, 1), (3, 2), (3, 5)]
