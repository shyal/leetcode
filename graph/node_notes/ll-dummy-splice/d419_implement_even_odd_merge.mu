# REFERENCE: d419 EPI 7.10 Implement even-odd merge
class Solution
  def even_odd_merge(L: ListNode?) -> ListNode?
    if not L
      return L
    even, odd = L, L.next
    odd_head = odd
    while odd and odd.next
      even.next = even = odd.next
      odd.next = odd = even.next
    even.next = odd_head
    L
