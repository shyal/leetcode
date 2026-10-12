"""
URL: https://leetcode.com/problems/linked-list-random-node/description/?envType=problem-list-v2&envId=vn57k9wr

382. Linked List Random Node

Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.

Implement the Solution class:

- Solution(ListNode head) Initializes the object with the head of the singly-linked list head.
- int getRandom() Chooses a node randomly from the list and returns its value. All the nodes of the list should be equally likely to be chosen.

Example 1:

Input
["Solution", "getRandom", "getRandom", "getRandom", "getRandom", "getRandom"]
[[[1, 2, 3]], [], [], [], [], []]
Output
[null, 1, 3, 2, 2, 3]

Explanation
Solution solution = new Solution([1, 2, 3]);
solution.getRandom(); // return 1
solution.getRandom(); // return 3
solution.getRandom(); // return 2
solution.getRandom(); // return 2
solution.getRandom(); // return 3
// getRandom() should return either 1, 2, or 3 randomly. Each element should have equal probability of returning.

Constraints:

- The number of nodes in the linked list will be in the range [1, 10^4].
- -10^4 <= Node.val <= 10^4
- At most 10^4 calls will be made to getRandom().

Follow up:

- What if the linked list is extremely large and its length is unknown to you?
- Could you solve this efficiently without using extra space?

---

LEETCODE: Accepted (11 ms, 23.3 MB)
"""

import random


# mu 0.10
# class Solution
#   def __init__(head: ListNode?)
#     self.head = head
#
#   def getRandom() -> int
#     curr = self.head
#     i = 1
#     val = 0
#     while curr
#       prob = 1/i
#       rand = random.random()
#       if rand < prob
#         val = curr.val
#       curr = curr.next
#       i += 1
#     return val

from collections import Counter
from typing import Optional


class Solution:
    def __init__(self, head: Optional[ListNode]):
        self.head = head

    def getRandom(self) -> int:
        curr = self.head
        i = 1
        val = 0
        while curr:
            prob = 1 / i
            rand = random.random()
            if rand < prob:
                val = curr.val
            curr = curr.next
            i += 1
        return val


head = build_linked_list([1, 2, 3])
print(head)
sol = Solution(head)
n = 30000
counts = Counter(sol.getRandom() for _ in range(n))
print(counts)
_l, _r = set(counts), {1, 2, 3}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
for v in counts.values():
    _l, _r = abs(v - n / 3), 0.03 * n
    assert _l < _r, f"left : {_l!r}\nright: {_r!r}\nop   : <"
