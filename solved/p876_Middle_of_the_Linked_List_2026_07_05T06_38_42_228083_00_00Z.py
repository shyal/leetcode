"""
URL: https://leetcode.com/problems/middle-of-the-linked-list/description/?envType=problem-list-v2&envId=vn57k9wr

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
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


sol = Solution()

draw_linked_list(sol.middleNode(build_linked_list([1, 2, 3, 4, 5])))  # 3 -> 4 -> 5

assert get_list_values(sol.middleNode(build_linked_list([1, 2, 3, 4, 5]))) == [3, 4, 5]
assert get_list_values(sol.middleNode(build_linked_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]
assert get_list_values(sol.middleNode(build_linked_list([1]))) == [1]
assert get_list_values(sol.middleNode(build_linked_list([1, 2]))) == [2]
assert get_list_values(sol.middleNode(build_linked_list([1, 2, 3]))) == [2, 3]
assert get_list_values(sol.middleNode(build_linked_list([1, 2, 3, 4]))) == [3, 4]
assert get_list_values(sol.middleNode(build_linked_list([100]))) == [100]
assert get_list_values(sol.middleNode(build_linked_list([5, 5, 5, 5, 5]))) == [5, 5, 5]
assert get_list_values(sol.middleNode(build_linked_list(list(range(1, 101))))) == list(range(51, 101))
assert get_list_values(sol.middleNode(build_linked_list(list(range(1, 100))))) == list(range(50, 100))
assert sol.middleNode(build_linked_list([1, 2])).val == 2
assert sol.middleNode(build_linked_list([1, 2, 3])).next.val == 3
assert sol.middleNode(build_linked_list([1])).next is None