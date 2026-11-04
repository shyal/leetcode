# URL: https://leetcode.com/problems/reorder-list/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 143. Reorder List
#
# You are given the head of a singly linked-list. The list can be represented as:
#
# L0 → L1 → … → Ln - 1 → Ln
#
# Reorder the list to be on the following form:
#
# L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
#
# You may not modify the values in the list's nodes. Only nodes themselves may be changed.
#
# Example 1:
#
# Input: head = [1,2,3,4]
# Output: [1,4,2,3]
#
# Example 2:
#
# Input: head = [1,2,3,4,5]
# Output: [1,5,2,4,3]
#
# Constraints:
#
#     The number of nodes in the list is in the range [1, 5 * 10^4].
#     1 <= Node.val <= 1000
#
# ---
# LEETCODE: Accepted (2 ms, 27.6 MB)

# mu 0.16

class Solution
  def reorderList(head: ListNode?) -> none
    fast = slow = head
    while fast and fast.next and fast.next.next
      fast = fast.next.next
      slow = slow.next
    second = slow.next
    slow.next = None
    second, _ = linked_list_reverse_k(second)
    a = head
    b = second
    while a and b
      a.next, b.next, a, b = b, a.next, a.next, b.next
    b

sol = Solution()

head1 = build_linked_list([1, 2, 3, 4])
print(head1)
sol.reorderList(head1)
print(get_list_values(head1))  # [1,4,2,3]

head2 = build_linked_list([1, 2, 3, 4, 5])
sol.reorderList(head2)
print(get_list_values(head2))  # [1,5,2,4,3]

assert get_list_values(build_linked_list([1, 2, 3, 4])) == [1, 2, 3, 4]
head = build_linked_list([1, 2, 3, 4])
sol.reorderList(head)
assert get_list_values(head) == [1, 4, 2, 3]

assert get_list_values(build_linked_list([1, 2, 3, 4, 5])) == [1, 2, 3, 4, 5]
head = build_linked_list([1, 2, 3, 4, 5])
sol.reorderList(head)
assert get_list_values(head) == [1, 5, 2, 4, 3]

head = build_linked_list([1])
sol.reorderList(head)
assert get_list_values(head) == [1]


head = build_linked_list([1, 2])
sol.reorderList(head)
assert get_list_values(head) == [1, 2]


head = build_linked_list([1, 2, 3])
sol.reorderList(head)
assert get_list_values(head) == [1, 3, 2]
