# REFERENCE: d181 Reverse Sublist
class Solution:
    def reverseSublist(self, h):
        d = ListNode()
        t = h
        while h:
            # don't hunt him = him don't hunt
            d.next, h.next, h = h, d.next, h.next
        # don't try
        return d.next, t
