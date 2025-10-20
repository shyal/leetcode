"""
URL: https://leetcode.com/problems/reverse-linked-list/description/

206. Reverse Linked List

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:

Input: head = [1,2]
Output: [2,1]

Example 3:

Input: head = []
Output: []

Constraints:

    The number of nodes in the list is the range [0, 5000].
    -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?
"""


class Solution:
    def reverseList(self, h: Optional[ListNode]) -> Optional[ListNode]:
        d = ListNode()
        while h:
            d.next, h.next, h = h, d.next, h.next
        return d.next


sol = Solution()

assert get_list_values(sol.reverseList(build_linked_list([1, 2, 3, 4, 5]))) == [
    5,
    4,
    3,
    2,
    1,
]
assert get_list_values(sol.reverseList(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.reverseList(build_linked_list([]))) == []
assert get_list_values(sol.reverseList(build_linked_list([42]))) == [42]
assert get_list_values(sol.reverseList(build_linked_list([-1, 0, 1]))) == [1, 0, -1]
assert get_list_values(sol.reverseList(build_linked_list([2, 2, 2]))) == [2, 2, 2]
assert get_list_values(sol.reverseList(build_linked_list([5000, -5000]))) == [
    -5000,
    5000,
]

assert get_list_values(sol.reverseList(build_linked_list([0]))) == [0]
