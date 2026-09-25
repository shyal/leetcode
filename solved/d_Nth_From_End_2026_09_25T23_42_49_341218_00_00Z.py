"""
DRILL: Nth From End

Given the head of a linked list and an integer n, return the value of the
nth node from the end. The last node is the 1st from the end.

Example 1:

Input: head = [1, 2, 3, 4, 5], n = 2
Output: 4

Example 2:

Input: head = [1, 2, 3, 4, 5], n = 5
Output: 1

Example 3:

Input: head = [1, 2, 3, 4, 5], n = 1
Output: 5

Constraints:

    1 <= number of nodes <= 3 * 10**4
    1 <= n <= number of nodes
    0 <= Node.val <= 100

    REQUIRED: one pass, O(1) extra space, two pointers n apart. NO length
    count, NO second walk, NO list of nodes.
---
Learning
"""


# mu 0.4
# def nthFromEnd(head: ListNode, n: int) -> int
#   w = f = head
#   for _ in range(n)
#     f = f.next
#   while f
#     w, f = w.next, f.next
#   return w.val
#

class Solution:
    def nthFromEnd(self, head: ListNode, n: int) -> int:
        w = f = head
        for _ in range(n):
            f = f.next
        while f:
            w, f = w.next, f.next
        return w.val


sol = Solution()
head = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(head)
print(sol.nthFromEnd(head, 2))
assert sol.nthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 2) == 4
assert sol.nthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 5) == 1
assert sol.nthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 1) == 5
assert sol.nthFromEnd(build_linked_list([9]), 1) == 9
assert sol.nthFromEnd(build_linked_list([1, 2]), 2) == 1
assert sol.nthFromEnd(build_linked_list([1, 2, 3, 4, 5, 6]), 3) == 4
assert sol.nthFromEnd(build_linked_list(list(range(0, 30000))), 30000) == 0
assert sol.nthFromEnd(build_linked_list(list(range(0, 30000))), 12345) == 30000 - 12345
