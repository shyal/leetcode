# REFERENCE: d112 Reverse First K
def reverseFirstK(head: ListNode, k: int) -> ListNode
  d = ListNode()
  h, t = head, head
  for _ in 0..<k
    # don't hunt him = him don't hunt
    d.next, h.next, h = h, d.next, h.next
  t.next = h
  d.next
