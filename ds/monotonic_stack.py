from operator import lt, gt, le, ge


class Type:
    decreasing = 0
    increasing = 1


class MonotonicStack:

    def __init__(self, type: Type = Type.increasing):
        self.data = []
        self.type = type

    def push(self, val):
        op = (lt, gt)[self.type]
        ope = (le, ge)[self.type]

        if not self.data or ope(val, self.data[-1]):
            self.data.append(val)
        else:
            while self.data and op(self.data[-1], val):
                self.data.pop()
            self.data.append(val)

    def pop(self):
        if self.data:
            return self.data.pop()

    def peek(self):
        if self.data:
            return self.data[-1]

    def __str__(self):
        return str(self.data)


stack = MonotonicStack(Type.decreasing)
stack.push(5)
stack.push(4)
stack.push(3)
stack.push(2)
stack.push(1)
stack.push(3)
assert stack.data == [5, 4, 3, 3]

stack = MonotonicStack(Type.increasing)
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)
stack.push(5)
stack.push(3)
assert stack.data == [1, 2, 3, 3]
