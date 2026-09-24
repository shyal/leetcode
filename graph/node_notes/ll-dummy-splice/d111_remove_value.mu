# REFERENCE: d111 Remove Value
def removeValue(head: ListNode?, val: int) -> ListNode?
  d = ListNode(0, head)
  pre = d
  while pre.next
    if pre.next.val == val
      pre.next = pre.next.next
    else
      pre = pre.next
  d.next
