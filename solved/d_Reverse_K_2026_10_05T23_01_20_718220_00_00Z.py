"""
DRILL: Reverse K

Given the head h of a linked list and an integer k, reverse the first k
nodes in place. Return the new head and the new tail, in that order. The
new tail is the node that was h, and its next is the first node that was
not reversed. A list with fewer than k nodes is reversed whole.

Example 1:

Input: h = [1, 2, 3, 4, 5], k = 3
Output: [3, 2, 1, 4, 5], tail 1

Example 2:

Input: h = [1, 2, 3, 4, 5], k = 5
Output: [5, 4, 3, 2, 1], tail 1

Example 3:

Input: h = [1, 2, 3], k = 1
Output: [1, 2, 3], tail 1

Example 4:

Input: h = [1, 2], k = 5
Output: [2, 1], tail 1

Constraints:

    0 <= number of nodes <= 5000
    1 <= k <= 10^4
    -5000 <= Node.val <= 5000
    An empty list returns None for both the head and the tail.

    REQUIRED: O(k) time, O(1) extra space, pointers flipped in place. NO
    list of nodes, NO recursion, NO writing to val.
"""


# mu 0.7
# def reverseK(h: ListNode?, k: int) -> (ListNode?, ListNode?)
#   d = ListNode()
#   t = h
#   while h and k
#     d.next, h.next, h = h, d.next, h.next
#     k -= 1
#   if t
#     t.next = h
#   d.next, t

from typing import Optional


class Solution:
    def reverseK(self, h: Optional[ListNode], k: int) -> tuple[Optional[ListNode], Optional[ListNode]]:
        d = ListNode()
        t = h
        while h and k:
            d.next, h.next, h = h, d.next, h.next
            k -= 1
        if t:
            t.next = h
        return d.next, t


sol = Solution()
h = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(h)
head, tail = sol.reverseK(h, 3)
print(get_list_values(head), tail.val)
def rev(vals, k):
    head, tail = sol.reverseK(build_linked_list(vals), k)
    after = tail.next.val if tail and tail.next else None
    return get_list_values(head), tail and tail.val, after
assert rev([1, 2, 3, 4, 5], 3) == ([3, 2, 1, 4, 5], 1, 4)
assert rev([1, 2, 3, 4, 5], 5) == ([5, 4, 3, 2, 1], 1, None)
assert rev([1, 2, 3], 1) == ([1, 2, 3], 1, 2)
assert rev([1, 2], 5) == ([2, 1], 1, None)
assert rev([1, 2, 3, 4], 2) == ([2, 1, 3, 4], 1, 3)
assert rev([7], 1) == ([7], 7, None)
assert rev([], 2) == ([], None, None)
assert rev([3, 3, 3], 2) == ([3, 3, 3], 3, 3)
assert rev(list(range(0, 5000)), 4999) == (list(range(4998, -1, -1)) + [4999], 0, 4999)
