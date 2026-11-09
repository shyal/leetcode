"""
EPI 8.9 Implement a queue with max API

Implement a queue of integers. Solution() makes an empty queue with
these methods:

    enqueue(x)   adds x at the back and returns nothing
    dequeue()    removes the value at the front and returns it
    max()        returns the largest value in the queue

The methods dequeue() and max() are called only on a queue that is not
empty.

Example 1:

    q = Solution()
    q.enqueue(3)
    q.enqueue(1)
    q.enqueue(2)
    q.max()       -> 3
    q.dequeue()   -> 3
    q.max()       -> 2

Example 2:

    q = Solution()
    q.enqueue(5)
    q.enqueue(5)
    q.dequeue()   -> 5
    q.max()       -> 5     (the second 5 is still in the queue)

Constraints:

    -10^9 <= x <= 10^9
    up to 3 * 10^5 calls

    REQUIRED: O(1) amortised time per call. NO max() over the stored
    values, NO heap, NO sort.
"""


class Solution:
    def enqueue(self, x: int) -> None:
        pass

    def dequeue(self) -> int:
        pass

    def max(self) -> int:
        pass


sol = Solution()

sol.enqueue(3)
sol.enqueue(1)
sol.enqueue(2)
print(sol.max())  # 3

# sol = Solution()
# sol.enqueue(3)
# sol.enqueue(1)
# sol.enqueue(2)
# assert sol.max() == 3
# assert sol.dequeue() == 3
# assert sol.max() == 2
# assert sol.dequeue() == 1
# assert sol.max() == 2
# assert sol.dequeue() == 2
# sol.enqueue(5)
# sol.enqueue(5)
# assert sol.dequeue() == 5 and sol.max() == 5
# sol.enqueue(-1)
# assert sol.max() == 5 and sol.dequeue() == 5
# assert sol.max() == -1
# sol.enqueue(4)
# assert sol.max() == 4 and sol.dequeue() == -1 and sol.max() == 4
# assert sol.dequeue() == 4
# _ = [sol.enqueue(x) for x in range(100000, 0, -1)]
# assert all(sol.max() == x and sol.dequeue() == x for x in range(100000, 0, -1))
# _ = [sol.enqueue(x) for x in range(100000)]
# assert all(sol.max() == 99999 and sol.dequeue() == x for x in range(99999))
# assert sol.max() == 99999 and sol.dequeue() == 99999
# _ = [sol.enqueue(x % 1000) for x in range(100000)]
# assert all(sol.max() == 999 and sol.dequeue() == x % 1000 for x in range(99000))
