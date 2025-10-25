"""
URL: https://leetcode.com/problems/reverse-linked-list-ii/description/?envType=problem-list-v2&envId=vn57k9wr

92. Reverse Linked List II

Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]

Example 2:

Input: head = [5], left = 1, right = 1
Output: [5]

Constraints:

    The number of nodes in the list is in the range [1, 500].
    -500 <= Node.val <= 500
    1 <= left <= right <= n, where n is the length of the list.

Follow up: Could you do it in one pass?
"""


class Solution:

    def reverseSubList(self, head):
        d = ListNode(-1)
        tail = head
        while head:
            d.next, head.next, head = head, d.next, head.next
        return d.next, tail

    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        if left == right:
            return head
        d = ListNode(-1, head)
        sub_start = d
        for _ in range(1, left):
            sub_start = sub_start.next
        sub_end = head
        for _ in range(1, right - 1):
            sub_end = sub_end.next
        tail = sub_end.next
        after = tail.next if tail else None
        if tail:
            tail.next = None
        sub_start.next, sub_end = self.reverseSubList(sub_start.next)
        if sub_end:
            sub_end.next = after
        return d.next


sol = Solution()
assert get_list_values(
    sol.reverseBetween(build_linked_list([1, 2, 3, 4, 5]), 2, 4)
) == [1, 4, 3, 2, 5]
assert get_list_values(sol.reverseBetween(build_linked_list([5]), 1, 1)) == [5]
assert get_list_values(
    sol.reverseBetween(build_linked_list([1, 2, 3, 4, 5]), 1, 5)
) == [5, 4, 3, 2, 1]
