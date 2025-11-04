"""
URL: https://leetcode.com/problems/remove-linked-list-elements/description/?envType=problem-list-v2&envId=vn57k9wr

203. Remove Linked List Elements

Given the head of a linked list and an integer val, remove all the nodes of the linked list that has Node.val == val, and return the new head.


Example 1:

Input: head = [1,2,6,3,4,5,6], val = 6
Output: [1,2,3,4,5]

Example 2:

Input: head = [], val = 1
Output: []

Example 3:

Input: head = [7,7,7,7], val = 7
Output: []


Constraints:

        The number of nodes in the list is in the range [0, 104].
        1 <= Node.val <= 50
        0 <= val <= 50
"""


class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy_head = ListNode(None, head)
        it = dummy_head
        while it.next:
            if it.next.val == val:
                it.next = it.next.next
            else:
                it = it.next
        return dummy_head.next


sol = Solution()
head = build_linked_list([1, 2, 6, 3, 4, 5, 6])
draw_linked_list(head)
assert get_list_values(sol.removeElements(head, 6)) == [1, 2, 3, 4, 5]
draw_linked_list(head)

head = build_linked_list([])
draw_linked_list(head)
assert get_list_values(sol.removeElements(head, 1)) == []

head = build_linked_list([7, 7, 7, 7])
draw_linked_list(head)
assert get_list_values(sol.removeElements(head, 7)) == []

head = build_linked_list([1, 2, 3, 4, 5, 5, 5, 5])
draw_linked_list(head)
assert get_list_values(sol.removeElements(head, 5)) == [1, 2, 3, 4]
draw_linked_list(head)

head = build_linked_list([5, 5, 5, 5, 1, 2, 3, 4])
draw_linked_list(head)
assert get_list_values(sol.removeElements(head, 5)) == [1, 2, 3, 4]
draw_linked_list(head)
