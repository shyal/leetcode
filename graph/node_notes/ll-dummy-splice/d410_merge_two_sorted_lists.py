# REFERENCE: d410 EPI 7.1 Merge two sorted lists
class Solution:
    def merge_two_sorted_lists(self, L1, L2):
        d = t = ListNode()
        while L1 and L2:
            if L1.val <= L2.val:
                t.next, L1 = L1, L1.next
            else:
                t.next, L2 = L2, L2.next
            t = t.next
        t.next = L1 or L2
        return d.next
