# REFERENCE: d111 Remove Value
class Solution:
    def removeValue(self, head, val):
        d = pre = ListNode(0, head)
        while pre.next:
            if pre.next.val == val:
                pre.next = pre.next.next
            else:
                pre = pre.next
        return d.next
