"""
DRILL: Interleave

Given the heads a and b of two linked lists, where b has as many nodes as
a or one fewer, weave them into one list that alternates a node of a and
a node of b, starting with a, and return its head. The nodes move; no
node is created.

Example 1:

Input: a = [1, 2, 3], b = [4, 5, 6]
Output: [1, 4, 2, 5, 3, 6]

Example 2:

Input: a = [1, 2, 3], b = [4, 5]
Output: [1, 4, 2, 5, 3]

Example 3:

Input: a = [1], b = []
Output: [1]

Constraints:

    1 <= number of nodes in a <= 5 * 10**4
    number of nodes in b is len(a) or len(a) - 1
    1 <= Node.val <= 1000

    REQUIRED: O(n) time, O(1) extra space, relink in place. NO new nodes,
    NO list of values.
---
Learning
"""


# mu 0.8
# class Solution
#   def interleave(a: ListNode, b: ListNode?) -> ListNode
#     head = a
#     while b
#       a.next, b.next, a, b = b, a.next, a.next, b.next
#     head

from typing import Optional


class Solution:
    def interleave(self, a: ListNode, b: Optional[ListNode]) -> ListNode:
        head = a
        while b:
            a.next, b.next, a, b = b, a.next, a.next, b.next
        return head


sol = Solution()
a = build_linked_list([1, 2, 3])
b = build_linked_list([4, 5])
draw_linked_list(a)
draw_linked_list(b)
print(get_list_values(sol.interleave(a, b)))
def weave(x, y):
    return get_list_values(sol.interleave(build_linked_list(x), build_linked_list(y)))
