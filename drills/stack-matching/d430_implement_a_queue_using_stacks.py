"""
EPI 8.8 Implement a queue using stacks

Implement a queue of integers with two stacks. A stack here is a Python
list that you change only with append(x) and pop() and read only with
[-1] and len(). Solution() makes an empty queue with these methods:

    enqueue(x)   adds x at the back and returns nothing
    dequeue()    removes the value at the front and returns it

The method dequeue() is called only on a queue that is not empty.

Example 1:

    q = Solution()
    q.enqueue(1)
    q.enqueue(2)
    q.dequeue()   -> 1
    q.enqueue(3)
    q.dequeue()   -> 2
    q.dequeue()   -> 3

Example 2:

    q = Solution()
    q.enqueue(5)
    q.dequeue()   -> 5

Constraints:

    -10^9 <= x <= 10^9
    up to 3 * 10^5 calls

    REQUIRED: O(1) amortised time per call. NO deque, NO pop(0), NO
    insert(), NO slicing, NO index other than [-1].
"""


class Solution:
    def enqueue(self, x: int) -> None:
        pass

    def dequeue(self) -> int:
        pass


sol = Solution()

sol.enqueue(1)
sol.enqueue(2)
print(sol.dequeue())  # 1

# sol = Solution()
# sol.enqueue(1)
# sol.enqueue(2)
# assert sol.dequeue() == 1
# sol.enqueue(3)
# assert sol.dequeue() == 2
# assert sol.dequeue() == 3
# sol.enqueue(5)
# assert sol.dequeue() == 5
# sol.enqueue(-1)
# sol.enqueue(-1)
# sol.enqueue(0)
# assert [sol.dequeue() for _ in range(3)] == [-1, -1, 0]
# sol.enqueue(6)
# sol.enqueue(7)
# assert sol.dequeue() == 6
# sol.enqueue(8)
# sol.enqueue(9)
# assert [sol.dequeue() for _ in range(3)] == [7, 8, 9]
# _ = [sol.enqueue(x) for x in range(100000)]
# assert all(sol.dequeue() == x for x in range(50000))
# _ = [sol.enqueue(x) for x in range(100000, 150000)]
# assert all(sol.dequeue() == x for x in range(50000, 150000))
# _ = [(sol.enqueue(x), sol.enqueue(x + 1), sol.dequeue()) for x in range(0, 100000, 2)]
# assert all(sol.dequeue() == x for x in range(50000, 100000))
