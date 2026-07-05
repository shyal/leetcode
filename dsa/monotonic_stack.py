from operator import lt, gt, le, ge


class Type:
    decreasing = 0
    increasing = 1


class MonotonicStack:

    def __init__(self, type: Type = Type.increasing):
        self.data = []
        self.type = type

    def push(self, val):
        res = []
        op = (lt, gt)[self.type]
        ope = (le, ge)[self.type]

        if not self.data or ope(val[0], self.data[-1][0]):
            self.data.append(val)
        else:
            while self.data and op(self.data[-1][0], val[0]):
                r = self.data.pop()
                res.append(r)
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
assert res == [(1, 4), (2, 3)] # these two got evicted by the last 3
assert stack.data == [(5, 0), (4, 1), (3, 2), (3, 5)]
