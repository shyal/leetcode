"""
DRILL: Reverse First K

Given the head of a linked list and an integer k, reverse the first k
nodes and return the new head. The remaining nodes keep their order and
stay attached after the reversed part.

Example 1:

Input: head = [1, 2, 3, 4, 5], k = 3
Output: [3, 2, 1, 4, 5]

Example 2:

Input: head = [1, 2, 3, 4, 5], k = 5
Output: [5, 4, 3, 2, 1]

Example 3:

Input: head = [1, 2, 3], k = 1
Output: [1, 2, 3]

Constraints:

    1 <= number of nodes <= 5000
    1 <= k <= number of nodes
    -1000 <= Node.val <= 1000

    REQUIRED: O(k) time, O(1) extra space, pointers flipped in place. NO
    list of nodes, NO recursion, NO writing to val.
---
Learning
"""


# mu 0.7
# def reverseSublist(head)
#   d = ListNode()
#   t = head
#   while head
#     d.next, head.next, head = head, d.next, head.next
#   d.next, t
#
# def reverseFirstK(head: ListNode, k: int) -> ListNode
#   d = ListNode()
#   h = t = head
#   while head
#     d.next, head.next, head = head, d.next, head.next
#   t.next = h
#   d.next

class Solution:
    def reverseSublist(self, head):
        d = ListNode()
        t = head
        while head:
            d.next, head.next, head = head, d.next, head.next
        return d.next, t

    def reverseFirstK(self, head: ListNode, k: int) -> ListNode:
        d = ListNode()
        h = t = head
        while head:
            d.next, head.next, head = head, d.next, head.next
        t.next = h
        return d.next


sol = Solution()
head = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(head)
print(get_list_values(sol.reverseFirstK(head, 3)))
def rev(vals, k):
    return get_list_values(sol.reverseFirstK(build_linked_list(vals), k))
