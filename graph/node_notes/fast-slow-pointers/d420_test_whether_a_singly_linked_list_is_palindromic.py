# REFERENCE: d420 EPI 7.11 Test whether a singly linked list is palindromic
class Solution:
    def is_linked_list_a_palindrome(self, L):
        slow = fast = L
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        back, _ = linked_list_reverse_k(slow)
        while back:
            if back.val != L.val:
                return False
            back, L = back.next, L.next
        return True
