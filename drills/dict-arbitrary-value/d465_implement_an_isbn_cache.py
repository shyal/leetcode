"""
EPI 12.3 Implement an ISBN cache

Implement a cache of book prices keyed by ISBN, with a fixed capacity.

- Solution(capacity) makes an empty cache that holds at most capacity
  entries.
- lookup(isbn) returns the price of isbn, or -1 when isbn is not in the
  cache.
- insert(isbn, price) adds isbn with its price. When isbn is already in
  the cache, its price does not change. When the cache is full and isbn
  is new, the least recently used entry is removed first.
- erase(isbn) removes isbn and returns True, or returns False when isbn
  is not in the cache.

A lookup or an insert of an ISBN in the cache makes it the most recently
used entry.

Example 1:

Input: Solution(2), insert(1, 10), insert(2, 20), lookup(1),
       insert(3, 30), lookup(2), lookup(1), lookup(3)
Output: None, None, 10, None, -1, 10, 30
Explanation: lookup(1) makes ISBN 1 more recent than ISBN 2, so
insert(3, 30) removes ISBN 2.

Example 2:

Input: Solution(2), insert(1, 10), insert(1, 99), lookup(1), erase(1),
       erase(1)
Output: None, None, 10, True, False
Explanation: the second insert of ISBN 1 keeps the price 10.

Constraints:

    1 <= capacity <= 10^5
    0 <= isbn, price <= 10^9
    At most 2 * 10^5 calls.

    REQUIRED: O(1) time for each call.
"""


class Solution:
    def __init__(self, capacity: int) -> None:
        pass

    def lookup(self, isbn: int) -> int:
        pass

    def insert(self, isbn: int, price: int) -> None:
        pass

    def erase(self, isbn: int) -> bool:
        pass


sol = Solution(2)

sol.insert(1, 10)
sol.insert(2, 20)
sol.lookup(1)
sol.insert(3, 30)
print(sol.lookup(2), sol.lookup(1), sol.lookup(3))  # -1 10 30

# sol = Solution(2)
# sol.insert(1, 10)
# sol.insert(2, 20)
# assert sol.lookup(1) == 10
# sol.insert(3, 30)
# assert sol.lookup(2) == -1
# assert sol.lookup(1) == 10
# assert sol.lookup(3) == 30
# sol.insert(1, 99)
# assert sol.lookup(1) == 10
# sol.insert(4, 40)
# assert sol.lookup(3) == -1
# assert sol.erase(1) is True
# assert sol.erase(1) is False
# assert sol.lookup(1) == -1
# sol.insert(5, 50)
# assert sol.lookup(4) == 40
# assert sol.lookup(5) == 50
# sol = Solution(1)
# assert sol.lookup(7) == -1
# sol.insert(7, 70)
# sol.insert(8, 80)
# assert sol.lookup(7) == -1
# assert sol.lookup(8) == 80
# assert sol.erase(9) is False
# sol.insert(9, 0)
# assert sol.lookup(9) == 0
# assert sol.erase(9) is True
# assert sol.lookup(8) == -1
# sol = Solution(3)
# sol.insert(1, 1)
# sol.insert(2, 2)
# sol.insert(3, 3)
# assert sol.erase(1) is True
# sol.insert(4, 4)
# assert sol.lookup(2) == 2
# sol.insert(5, 5)
# assert sol.lookup(3) == -1
# assert sol.lookup(2) == 2
# sol = Solution(1000)
# _ = [sol.insert(i, 2 * i) for i in range(10 ** 5)]
# assert sol.lookup(98999) == -1
# assert sol.lookup(99000) == 198000
# _ = [sol.lookup(99000) for _ in range(10 ** 5)]
# sol.insert(10 ** 6, 7)
# assert sol.lookup(99000) == 198000
# assert sol.lookup(99001) == -1
