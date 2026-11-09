# REFERENCE: d421 EPI 7.12 Implement list pivoting
class Solution:
    def list_pivoting(self, l, x):
        heads = [ListNode(), ListNode(), ListNode()]
        tails = heads[:]
        while l:
            i = 0 if l.val < x else 1 if l.val == x else 2
            tails[i].next = tails[i] = l
            l = l.next
        tails[2].next = None
        tails[1].next = heads[2].next
        tails[0].next = heads[1].next
        return heads[0].next
