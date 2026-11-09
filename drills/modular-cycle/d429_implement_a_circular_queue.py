"""
EPI 8.7 Implement a circular queue

Implement a queue of integers that stores its values in a list used as
a ring. Solution(capacity) makes an empty queue with room for capacity
values, with these methods:

    enqueue(x)   adds x at the back and returns nothing
    dequeue()    removes the value at the front and returns it
    size()       returns the number of values in the queue

When the queue is full, enqueue first makes the list larger and keeps
the order of the values. The method dequeue() is called only on a
queue that is not empty.

Example 1:

    q = Solution(3)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()   -> 1
    q.enqueue(4)        (the list is full again)
    q.enqueue(5)        (the list grows)
    q.dequeue()   -> 2
    q.size()      -> 3

Example 2:

    q = Solution(1)
    q.size()      -> 0
    q.enqueue(7)
    q.dequeue()   -> 7

Constraints:

    1 <= capacity <= 10^5
    -10^9 <= x <= 10^9
    up to 3 * 10^5 calls

    REQUIRED: O(1) amortised time per call, O(capacity + size) space. NO
    deque, NO append(), pop() or insert() on the list of values.
"""


class Solution:
    def __init__(self, capacity: int) -> None:
        pass

    def enqueue(self, x: int) -> None:
        pass

    def dequeue(self) -> int:
        pass

    def size(self) -> int:
        pass


sol = Solution(3)

sol.enqueue(1)
sol.enqueue(2)
sol.enqueue(3)
print(sol.dequeue())  # 1

# sol = Solution(3)
# sol.enqueue(1)
# sol.enqueue(2)
# sol.enqueue(3)
# assert sol.dequeue() == 1
# sol.enqueue(4)
# sol.enqueue(5)
# assert sol.dequeue() == 2
# assert sol.size() == 3
# assert sol.dequeue() == 3 and sol.dequeue() == 4 and sol.dequeue() == 5
# assert sol.size() == 0
# sol = Solution(1)
# assert sol.size() == 0
# sol.enqueue(7)
# assert sol.size() == 1 and sol.dequeue() == 7 and sol.size() == 0
# sol.enqueue(8)
# sol.enqueue(9)
# sol.enqueue(10)
# assert sol.size() == 3 and sol.dequeue() == 8
# sol.enqueue(11)
# assert [sol.dequeue() for _ in range(3)] == [9, 10, 11]
# sol = Solution(2)
# sol.enqueue(1)
# assert sol.dequeue() == 1
# sol.enqueue(2)
# sol.enqueue(3)
# sol.enqueue(4)
# assert [sol.dequeue() for _ in range(3)] == [2, 3, 4]
# sol = Solution(1)
# _ = [sol.enqueue(x) for x in range(100000)]
# assert sol.size() == 100000
# assert all(sol.dequeue() == x for x in range(50000))
# _ = [sol.enqueue(x) for x in range(100000, 150000)]
# assert sol.size() == 100000
# assert all(sol.dequeue() == x for x in range(50000, 150000))
# assert sol.size() == 0
# sol = Solution(100000)
# _ = [(sol.enqueue(x), sol.dequeue()) for x in range(200000)]
# assert sol.size() == 0
