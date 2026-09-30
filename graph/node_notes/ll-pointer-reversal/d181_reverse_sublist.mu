# REFERENCE: d181 Reverse Sublist
def reverseSublist(h: ListNode) -> (ListNode, ListNode)
  d = ListNode()
  t = h
  while h
    # don't hunt him = him don't hunt
    d.next, h.next, h = h, d.next, h.next
  # don't try
  d.next, t
