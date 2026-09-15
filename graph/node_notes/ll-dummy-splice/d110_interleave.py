# REFERENCE: d110 Interleave
class Solution:
    def interleave(self, a, b):
        head = a
        while b:
            a.next, b.next, a, b = b, a.next, a.next, b.next
        return head
