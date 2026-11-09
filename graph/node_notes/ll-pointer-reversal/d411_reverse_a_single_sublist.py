# REFERENCE: d411 EPI 7.2 Reverse a single sublist
class Solution:
    def reverse_sublist(self, L, start, finish):
        d = pre = ListNode(0, L)
        for _ in range(start - 1):
            pre = pre.next
        pre.next, _ = linked_list_reverse_k(pre.next, finish - start + 1)
        return d.next
