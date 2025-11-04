"""
URL: https://leetcode.com/problems/middle-of-the-linked-list/description/

876. Middle of the Linked List

Given the head of a singly linked list, return the middle node of the linked list.

If there are two middle nodes, return the second middle node.


Example 1:

Input: head = [1,2,3,4,5]
Output: [3,4,5]
Explanation: The middle node of the list is node 3.

Example 2:

Input: head = [1,2,3,4,5,6]
Output: [4,5,6]
Explanation: Since the list has two middle nodes with values 3 and 4, we return the second one.


Constraints:

    The number of nodes in the list is in the range [1, 100].
    1 <= Node.val <= 100
"""


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


sol = Solution()

head = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(head)
assert get_list_values(sol.middleNode(head)) == [3, 4, 5]

head = build_linked_list([1, 2, 3, 4, 5, 6])
draw_linked_list(head)
assert get_list_values(sol.middleNode(head)) == [4, 5, 6]

head = build_linked_list([1, 2, 3])
draw_linked_list(head)
assert get_list_values(sol.middleNode(head)) == [2, 3]

head = build_linked_list([1, 2])
draw_linked_list(head)
assert get_list_values(sol.middleNode(head)) == [2]


head = build_linked_list([1, 2, 3, 4, 5, 6, 7])
draw_linked_list(head)
assert get_list_values(sol.middleNode(head)) == [4, 5, 6, 7]
