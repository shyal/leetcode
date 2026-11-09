# REFERENCE: d421 EPI 7.12 Implement list pivoting
class Solution
  def list_pivoting(l: ListNode?, x: int) -> ListNode?
    heads = [ListNode(), ListNode(), ListNode()]
    tails = heads[:]
    while l
      i = l.val < x ? 0 : l.val == x ? 1 : 2
      tails[i].next = tails[i] = l
      l = l.next
    tails[2].next = none
    tails[1].next = heads[2].next
    tails[0].next = heads[1].next
    heads[0].next
