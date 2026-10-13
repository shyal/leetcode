"""
DRILL: Remove Value

Given the head of a linked list and an integer val, remove every node
whose value is val and return the head of what remains. The removed
nodes may be at the head, in the middle, at the tail, or everywhere.

Example 1:

Input: head = [1, 2, 6, 3, 4, 5, 6], val = 6
Output: [1, 2, 3, 4, 5]

Example 2:

Input: head = [7, 7, 7, 7], val = 7
Output: []

Example 3:

Input: head = [7, 1, 7, 2], val = 7
Output: [1, 2]

Constraints:

    0 <= number of nodes <= 10**4
    1 <= Node.val <= 50
    1 <= val <= 50

    REQUIRED: one pass, O(1) extra space, one loop with NO special case
    for the head. NO list of values, NO second list.
---
Learning
"""


# mu 0.10
# class Solution
#   def removeValue(head: ListNode?, val: int) -> ListNode?
#     d = pre = ListNode(next=head)
#     while pre.next
#       if pre.next.val == val
#         pre.next = pre.next.next
#       else
#         pre = pre.next
#     d.next
#

from typing import Optional


class Solution:
    def removeValue(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        d = pre = ListNode(next=head)
        while pre.next:
            if pre.next.val == val:
                pre.next = pre.next.next
            else:
                pre = pre.next
        return d.next


sol = Solution()
head = build_linked_list([7, 1, 7, 2])
draw_linked_list(head)
print(get_list_values(sol.removeValue(head, 7)))
def rm(vals, val):
    return get_list_values(sol.removeValue(build_linked_list(vals), val))
_l, _r = rm([1, 2, 6, 3, 4, 5, 6], 6), [1, 2, 3, 4, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([7, 7, 7, 7], 7), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([7, 1, 7, 2], 7), [1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([], 1), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([1], 1), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([1], 2), [1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([1, 2, 3], 2), [1, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([1, 2, 3], 3), [1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([2, 2, 1, 2, 2], 2), [1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = rm([1, 2] * 5000, 2), [1] * 5000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
