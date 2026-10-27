# Given the head of a linked list and an integer k, reverse the first k
# nodes and return the new head. The order of the remaining nodes does not
# change, and they follow the reversed part.
#
# Example 1:
#
# Input: head = [1, 2, 3, 4, 5], k = 3
# Output: [3, 2, 1, 4, 5]
#
# Example 2:
#
# Input: head = [1, 2, 3, 4, 5], k = 5
# Output: [5, 4, 3, 2, 1]
#
# Example 3:
#
# Input: head = [1, 2, 3], k = 1
# Output: [1, 2, 3]
#
# Constraints:
#
#     1 <= number of nodes <= 5000
#     1 <= k <= number of nodes
#     -1000 <= Node.val <= 1000
#
#     REQUIRED: O(k) time, O(1) extra space, pointers flipped in place. NO
#     list of nodes, NO recursion, NO writing to val.
#
# ---

# mu 0.13

class Solution
  def reverseFirstK(h: ListNode, k: int) -> ListNode
    d = ListNode()
    t = h
    while h and k
      d.next, h.next, h, = h, d.next, h.next
      k -= 1
    if h
      t.next = h
    d.next

sol = Solution()

head = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(head)
print(get_list_values(sol.reverseFirstK(head, 3)))  # [3, 2, 1, 4, 5]

def rev(vals, k)
  return get_list_values(sol.reverseFirstK(build_linked_list(vals), k))

assert rev([1, 2, 3, 4, 5], 3) == [3, 2, 1, 4, 5]
assert rev([1, 2, 3, 4, 5], 5) == [5, 4, 3, 2, 1]
assert rev([1, 2, 3], 1) == [1, 2, 3]
assert rev([1], 1) == [1]
assert rev([1, 2], 2) == [2, 1]
assert rev([1, 2, 3, 4], 2) == [2, 1, 3, 4]
assert rev([1, 2, 3, 4], 3) == [3, 2, 1, 4]
assert rev(list(0..<5000), 4999) == list(range(4998, -1, -1)) + [4999]
