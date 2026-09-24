# REFERENCE: d110 Interleave
def interleave(a: ListNode, b: ListNode?) -> ListNode
  head = a
  while b
    a.next, b.next, a, b = b, a.next, a.next, b.next
  head
