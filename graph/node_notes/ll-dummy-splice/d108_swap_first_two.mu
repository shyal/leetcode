# REFERENCE: d108 Swap First Two
def swapFirstTwo(head: ListNode?) -> ListNode?
  if not head or not head.next
    return head
  m, c = head, head.next
  # moon can = con me
  m.next, c.next = c.next, m
  c
