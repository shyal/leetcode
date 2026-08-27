"""
URL: https://leetcode.com/problems/maximum-frequency-stack/description/?envType=problem-list-v2&envId=vn57k9wr

895. Maximum Frequency Stack

Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.

Implement the FreqStack class:

- FreqStack() constructs an empty frequency stack.
- void push(int val) pushes an integer val onto the top of the stack.
- int pop() removes and returns the most frequent element in the stack.
  - If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.

Example 1:

Input:
["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"]
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]

Output:
[null,null,null,null,null,null,null,5,7,5,4]

Explanation:
FreqStack freqStack = new FreqStack();
freqStack.push(5); // The stack is [5]
freqStack.push(7); // The stack is [5,7]
freqStack.push(5); // The stack is [5,7,5]
freqStack.push(7); // The stack is [5,7,5,7]
freqStack.push(4); // The stack is [5,7,5,7,4]
freqStack.push(5); // The stack is [5,7,5,7,4,5]
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
freqStack.pop();   // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
freqStack.pop();   // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].

Constraints:

- 0 <= val <= 10^9
- At most 2 * 10^4 calls will be made to push and pop.
- It is guaranteed that there will be at least one element in the stack before calling pop.

---

Ok so the constraints are hard. We need frequency, and ordering. This could be a monotonic stack
problem.

Monotonically increasing stack storing:

[frequency, value]

or:

[frequency, set([values, ...])]

if we use [frequency, value] we'll need to work extra hard for ties.

if we use [frequency, set([values, ...])] ties are easier to handle.

So let's try with [frequency, set([values, ...])]

It's also weird that the question doesn't give time complexity constraints.

Actually [frequency, list([values, ...])] would be better, as it would keep.. no
both the set and list version cannot maintain the tie requirement.

So back to [frequency, value], which is not so much a monotonic stack as much as
just a list of [frequency, value]. What makes it complex is having to track counts
using a dict and keep that in sync.

"""


class FreqStack:

    def __init__(self):
        self.stack = []
        self.count = defaultdict(int)

    def push(self, val: int) -> None:
        self.count[val] += 1
        if not self.stack:
            self.stack.append((1, val))
            return

        ind = bisect_right(self.stack, self.count[val], key=lambda x: x[0])
        self.stack.insert(ind, (self.count[val], val))

    def pop(self) -> int:
        _, val = self.stack.pop()
        self.count[val] -= 1
        return val


sol = FreqStack()

sol.push(5)
sol.push(7)
sol.push(5)
sol.push(7)
sol.push(4)
sol.push(5)

print(sol.stack)
print(sol.pop())  # 5
print(sol.pop())  # 7
print(sol.pop())  # 5
print(sol.pop())  # 4

# Testing all example calls as asserts
fs = FreqStack()
fs.push(5)  # stack: [5]
fs.push(7)  # stack: [5,7]
fs.push(5)  # stack: [5,7,5]
fs.push(7)  # stack: [5,7,5,7]
fs.push(4)  # stack: [5,7,5,7,4]
fs.push(5)  # stack: [5,7,5,7,4,5]
assert fs.pop() == 5  # most frequent is 5, stack becomes [5,7,5,7,4]
assert (
    fs.pop() == 7
)  # 5 and 7 are most frequent, 7 is closest to top, stack becomes [5,7,5,4]
assert fs.pop() == 5  # most frequent is 5, stack becomes [5,7,4]
assert fs.pop() == 4  # 4,5,7 are most frequent, 4 closest to top, stack becomes [5,7]
