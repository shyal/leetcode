# REFERENCE: d418 EPI 7.9 Implement cyclic right shift for singly linked lists
class Solution
  def cyclically_right_shift_list(L: ListNode?, k: int) -> ListNode?
    if not L
      return L
    tail, n = L, 1
    while tail.next
      tail, n = tail.next, n + 1
    k %= n
    if k == 0
      return L
    tail.next = L
    for _ in 0..<n - k
      tail = tail.next
    L, tail.next = tail.next, none
    L
