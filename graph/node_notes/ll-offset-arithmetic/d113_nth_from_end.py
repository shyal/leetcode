# REFERENCE: d113 Nth From End
class Solution:
    def nthFromEnd(self, head, n):
        w = f = head
        for _ in range(n):
            f = f.next
        while f:
            w, f = w.next, f.next
        return w.val
