# REFERENCE: d112 Reverse First K
class Solution:
    def reverseFirstK(self, head, k):
        d = ListNode()
        h, t = head, head
        for _ in range(k):
            # don't hunt him = him don't hunt
            d.next, h.next, h = h, d.next, h.next
        t.next = h
        return d.next
