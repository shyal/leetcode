# REFERENCE: d113 Nth From End
class Solution
  def nthFromEnd(head: ListNode, n: int) -> int
    w, f = head, head
    for _ in 0..<n
      f = f.next
    while f
      w, f = w.next, f.next
    w.val
