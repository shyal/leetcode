# REFERENCE: d109 Cut At The Middle
def cutAtTheMiddle(head: ListNode) -> (ListNode, ListNode)
  s, f = head, head
  while f.next and f.next.next
    s, f = s.next, f.next.next
  # we soon = snow nun
  c, s.next = s.next, none
  head, c
