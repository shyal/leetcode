"""
URL: https://leetcode.com/problems/delete-node-in-a-linked-list/

237. Delete Node in a Linked List

There is a singly-linked list head and we want to delete a node node in it.

You are given the node to be deleted node. You will not be given access to the first node of head.

All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list.

Delete the given node. Note that by deleting the node, we do not mean removing it from memory. We mean:

    The value of the given node should not exist in the linked list.
    The number of nodes in the linked list should decrease by one.
    All the values before node should remain the same in their order.
    All the values after node should remain the same in their order.

Example 1:

Input: head = [4,5,1,9], node = 5
Output: [4,1,9]
Explanation: You are given the second node with value 5, the linked list should become 4 -> 1 -> 9 after calling your function.

Example 2:

Input: head = [4,5,1,9], node = 1
Output: [4,5,9]
Explanation: You are given the third node with value 1, the linked list should become 4 -> 5 -> 9 after calling your function.

Constraints:

    The number of the nodes in the given list is in the range [2, 1000].
    -1000 <= Node.val <= 1000
    The value of each node in the list is unique.
    The node to be deleted is in the list and is not a tail node.
"""


class Solution:
    def deleteNode(self, node):
        last = None
        while node.next:
            if node.next.next is None:
                last = node
            node.val = node.next.val
            node = node.next
        last.next = None


sol = Solution()

head = build_linked_list([4, 5, 1, 9])
node = head.next
sol.deleteNode(node)
# print(get_list_values(head))  # [4, 1, 9]

head = build_linked_list([4, 5, 1, 9])
node = head.next
sol.deleteNode(node)
assert get_list_values(head) == [4, 1, 9]

head = build_linked_list([4, 5, 1, 9])
node = head.next.next
sol.deleteNode(node)
assert get_list_values(head) == [4, 5, 9]

head = build_linked_list([1, 2])
node = head
sol.deleteNode(node)
assert get_list_values(head) == [2]
head = build_linked_list([3, 4, 5])
node = head
sol.deleteNode(node)
assert get_list_values(head) == [4, 5]
head = build_linked_list([3, 4, 5])
node = head.next
sol.deleteNode(node)
assert get_list_values(head) == [3, 5]
head = build_linked_list([-1, 0, 1])
node = head.next
sol.deleteNode(node)
assert get_list_values(head) == [-1, 1]
head = build_linked_list([10, 20, 30, 40])
node = head.next.next
sol.deleteNode(node)
assert get_list_values(head) == [10, 20, 40]
head = build_linked_list([-1000, 1000])
node = head
sol.deleteNode(node)
assert get_list_values(head) == [1000]
head = build_linked_list([0, 1, -1])
node = head
sol.deleteNode(node)
assert get_list_values(head) == [1, -1]
head = build_linked_list([1000, 500, 0, -500, -1000])
node = head.next.next
sol.deleteNode(node)
assert get_list_values(head) == [1000, 500, -500, -1000]
