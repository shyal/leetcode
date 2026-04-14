"""
URL: https://leetcode.com/problems/implement-queue-using-stacks/description/?envType=problem-list-v2&envId=vn57k9wr

232. Implement Queue using Stacks

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).

Implement the MyQueue class:

- void push(int x) Pushes element x to the back of the queue.
- int pop() Removes the element from the front of the queue and returns it.
- int peek() Returns the element at the front of the queue.
- boolean empty() Returns true if the queue is empty, false otherwise.

Notes:

- You must use only standard operations of a stack, which means only push to top, peek/pop from top, size, and is empty operations are valid.
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

Example 1:

Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]

Explanation
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false

Constraints:

- 1 <= x <= 9
- At most 100 calls will be made to push, pop, peek, and empty.
- All the calls to pop and peek are valid.

Follow-up: Can you implement the queue such that each operation is amortized O(1) time complexity? In other words, performing n operations will take overall O(n) time even if one of those operations may take longer.
"""


class MyQueue:

    def __init__(self):
        self.stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        val = self.stack[0]
        self.stack = self.stack = self.stack[1:]
        return val

    def peek(self) -> int:
        return self.stack[0]

    def empty(self) -> bool:
        return len(self.stack) == 0


sol = MyQueue()
ops = ["MyQueue", "push", "push", "peek", "pop", "empty"]
args = [[], [1], [2], [], [], []]
results = []
for op, arg in zip(ops, args):
    if op == "MyQueue":
        results.append(None)
    elif op == "push":
        sol.push(arg[0])
        results.append(None)
    elif op == "peek":
        results.append(sol.peek())
    elif op == "pop":
        results.append(sol.pop())
    elif op == "empty":
        results.append(sol.empty())
# print(results)
# assert results == [None, None, None, 1, 1, False]

sol = MyQueue()
ops = ["MyQueue", "empty"]
args = [[], []]
results = []
for op, arg in zip(ops, args):
    if op == "MyQueue":
        results.append(None)
    elif op == "push":
        sol.push(arg[0])
        results.append(None)
    elif op == "peek":
        results.append(sol.peek())
    elif op == "pop":
        results.append(sol.pop())
    elif op == "empty":
        results.append(sol.empty())
# print(results)
# assert results == [None, True]

sol = MyQueue()
ops = ["MyQueue", "push", "peek", "pop", "empty"]
args = [[], [1], [], [], []]
results = []
for op, arg in zip(ops, args):
    if op == "MyQueue":
        results.append(None)
    elif op == "push":
        sol.push(arg[0])
        results.append(None)
    elif op == "peek":
        results.append(sol.peek())
    elif op == "pop":
        results.append(sol.pop())
    elif op == "empty":
        results.append(sol.empty())
# print(results)
assert results == [None, None, 1, 1, True]

sol = MyQueue()
ops = ["MyQueue", "push", "push", "pop", "push", "peek", "pop", "peek", "pop", "empty"]
args = [[], [1], [2], [], [3], [], [], [], [], []]
results = []
for op, arg in zip(ops, args):
    if op == "MyQueue":
        results.append(None)
    elif op == "push":
        sol.push(arg[0])
        results.append(None)
    elif op == "peek":
        results.append(sol.peek())
    elif op == "pop":
        results.append(sol.pop())
    elif op == "empty":
        results.append(sol.empty())
# print(results)
assert results == [None, None, None, 1, None, 2, 2, 3, 3, True]

sol = MyQueue()
ops = ["MyQueue", "push", "pop", "empty", "push", "peek", "push", "pop", "peek", "pop", "empty"]
args = [[], [1], [], [], [2], [], [3], [], [], [], []]
results = []
for op, arg in zip(ops, args):
    if op == "MyQueue":
        results.append(None)
    elif op == "push":
        sol.push(arg[0])
        results.append(None)
    elif op == "peek":
        results.append(sol.peek())
    elif op == "pop":
        results.append(sol.pop())
    elif op == "empty":
        results.append(sol.empty())
# print(results)
assert results == [None, None, 1, True, None, 2, None, 2, 3, 3, True]