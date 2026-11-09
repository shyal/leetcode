# REFERENCE: d416 EPI 7.7 Remove the kth last element from a list
class Solution
  def remove_kth_last(L: ListNode, k: int) -> ListNode?
    d = slow = ListNode(0, L)
    fast = L
    for _ in 0..<k
      fast = fast.next
    while fast
      slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    d.next
