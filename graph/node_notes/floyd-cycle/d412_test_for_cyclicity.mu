# REFERENCE: d412 EPI 7.3 Test for cyclicity
class Solution
  def has_cycle(head: ListNode?) -> ListNode?
    slow = fast = head
    while fast and fast.next
      slow, fast = slow.next, fast.next.next
      if slow is fast
        slow = head
        while slow is not fast
          slow, fast = slow.next, fast.next
        return slow
    none
