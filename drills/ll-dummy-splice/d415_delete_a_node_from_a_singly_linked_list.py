"""
EPI 7.6 Delete a node from a singly linked list

Given a node node_to_delete of a linked list, delete it from the list in
place and return nothing. You do not get the head of the list, and the
node is not the tail. After the call, a walk from the head gives the
values of the list in the same order, without the value of
node_to_delete.

Example 1:

Input: head = [3, 5, 7, 11], node_to_delete = the node 5
Output: head = [3, 7, 11]

Example 2:

Input: head = [3, 5, 7, 11], node_to_delete = the node 3
Output: head = [5, 7, 11]

Example 3:

Input: head = [1, 2], node_to_delete = the node 1
Output: head = [2]

Constraints:

    2 <= number of nodes <= 10^5
    -10^9 <= Node.val <= 10^9
    node_to_delete is not the tail.

    REQUIRED: O(1) time, O(1) extra space.
"""


class Solution:
    def deletion_from_list(self, node_to_delete: ListNode) -> None:
        pass


sol = Solution()

head = build_linked_list([3, 5, 7, 11])
sol.deletion_from_list(head.next)
print(get_list_values(head))  # [3, 7, 11]

# head = build_linked_list([3, 5, 7, 11])
# sol.deletion_from_list(head.next)
# assert get_list_values(head) == [3, 7, 11]
# head = build_linked_list([3, 5, 7, 11])
# sol.deletion_from_list(head)
# assert get_list_values(head) == [5, 7, 11]
# head = build_linked_list([3, 5, 7, 11])
# sol.deletion_from_list(head.next.next)
# assert get_list_values(head) == [3, 5, 11]
# head = build_linked_list([1, 2])
# sol.deletion_from_list(head)
# assert get_list_values(head) == [2]
# head = build_linked_list([1, 2, 3])
# sol.deletion_from_list(head.next)
# assert get_list_values(head) == [1, 3]
# head = build_linked_list([4, 4, 4])
# sol.deletion_from_list(head.next)
# assert get_list_values(head) == [4, 4]
# head = build_linked_list([1, 2, 3, 4, 5])
# sol.deletion_from_list(head.next.next.next)
# assert get_list_values(head) == [1, 2, 3, 5]
# sol.deletion_from_list(head)
# assert get_list_values(head) == [2, 3, 5]
# sol.deletion_from_list(head.next)
# assert get_list_values(head) == [2, 5]
# head = build_linked_list(list(range(10 ** 5)))
# sol.deletion_from_list(head)
# assert get_list_values(head) == list(range(1, 10 ** 5))
