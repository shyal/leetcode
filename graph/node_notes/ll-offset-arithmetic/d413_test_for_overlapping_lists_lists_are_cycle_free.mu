# REFERENCE: d413 EPI 7.4 Test for overlapping lists - lists are cycle-free
class Solution
  def overlapping_no_cycle_lists(l0: ListNode?, l1: ListNode?) -> ListNode?
    def length(h)
      n = 0
      while h
        n, h = n + 1, h.next
      n
    n0, n1 = length(l0), length(l1)
    if n0 < n1
      l0, l1, n0, n1 = l1, l0, n1, n0
    for _ in 0..<n0 - n1
      l0 = l0.next
    while l0 is not l1
      l0, l1 = l0.next, l1.next
    l0
