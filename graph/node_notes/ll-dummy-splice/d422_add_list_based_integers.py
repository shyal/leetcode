# REFERENCE: d422 EPI 7.13 Add list-based integers
class Solution:
    def add_two_numbers(self, L1, L2):
        d = t = ListNode()
        carry = 0
        while L1 or L2 or carry:
            carry += (L1.val if L1 else 0) + (L2.val if L2 else 0)
            carry, digit = divmod(carry, 10)
            t.next = t = ListNode(digit)
            L1, L2 = L1 and L1.next, L2 and L2.next
        return d.next
