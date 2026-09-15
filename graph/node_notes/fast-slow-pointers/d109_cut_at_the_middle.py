# REFERENCE: d109 Cut At The Middle
class Solution:
    def cutAtTheMiddle(self, head):
        s = f = head
        while f.next and f.next.next:
            s, f = s.next, f.next.next
        # we soon = snow nun
        c, s.next = s.next, None
        return head, c
