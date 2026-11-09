# REFERENCE: d484 EPI 13.11 Implement a fast sorting algorithm for lists
class Solution
  def stable_sort_list(L: ListNode?) -> ListNode?
    if not L or not L.next
      return L
    slow, fast = L, L.next
    while fast and fast.next
      slow, fast = slow.next, fast.next.next
    right, slow.next = slow.next, none
    a, b = self.stable_sort_list(L), self.stable_sort_list(right)
    tail = dummy = ListNode()
    while a and b
      if b.val < a.val
        tail.next, b = b, b.next
      else
        tail.next, a = a, a.next
      tail = tail.next
    tail.next = a or b
    dummy.next
