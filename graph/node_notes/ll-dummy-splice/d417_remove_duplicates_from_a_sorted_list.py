# REFERENCE: d417 EPI 7.8 Remove duplicates from a sorted list
class Solution:
    def remove_duplicates(self, L):
        it = L
        while it and it.next:
            if it.next.val == it.val:
                it.next = it.next.next
            else:
                it = it.next
        return L
