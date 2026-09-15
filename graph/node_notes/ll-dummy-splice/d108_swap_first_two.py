# REFERENCE: d108 Swap First Two
class Solution:
    def swapFirstTwo(self, head):
        if not head or not head.next:
            return head
        m, c = head, head.next
        # moon can = con me
        m.next, c.next = c.next, m
        return c
