# REFERENCE: d414 EPI 7.5 Test for overlapping lists - lists may have cycles
class Solution
  def overlapping_lists(l0: ListNode?, l1: ListNode?) -> ListNode?
    def cycle_start(h)
      slow = fast = h
      while fast and fast.next
        slow, fast = slow.next, fast.next.next
        if slow is fast
          slow = h
          while slow is not fast
            slow, fast = slow.next, fast.next
          return slow
      none
    def length(h)
      n = 0
      while h
        n, h = n + 1, h.next
      n
    c0, c1 = cycle_start(l0), cycle_start(l1)
    if not c0 and not c1
      n0, n1 = length(l0), length(l1)
      if n0 < n1
        l0, l1, n0, n1 = l1, l0, n1, n0
      for _ in 0..<n0 - n1
        l0 = l0.next
      while l0 is not l1
        l0, l1 = l0.next, l1.next
      return l0
    if not c0 or not c1
      return none
    t = c0.next
    while t is not c0 and t is not c1
      t = t.next
    t is c1 ? c1 : none
