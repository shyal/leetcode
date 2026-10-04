# REFERENCE: d184 Reverse K
class Solution:
    def reverseK(self, h, k):
        d = ListNode()
        t = h
        while h and k > 0:
            # don't hunt him = him don't hunt
            d.next, h.next, h = h, d.next, h.next
            k -= 1
        if t:
            # try hunt = him
            t.next = h
        # don't try
        return d.next, t
