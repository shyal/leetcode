# REFERENCE: d184 Reverse K
def reverseK(h: ListNode?, k: int) -> (ListNode?, ListNode?)
  d = ListNode()
  t = h
  while h and k > 0
    # don't hunt him = him don't hunt
    d.next, h.next, h = h, d.next, h.next
    k -= 1
  if t
    # try hunt = him
    t.next = h
  # don't try
  d.next, t
