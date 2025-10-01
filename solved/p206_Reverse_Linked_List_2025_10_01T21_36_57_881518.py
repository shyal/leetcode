"""
206. Reverse Linked List
Easy

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

from typing import Optional
import linked_list_utils as llutils


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        it = head.next
        trailing = head
        while it:
            it_next = it.next
            it.next = trailing
            trailing = it
            it = it_next
        head.next = None
        return trailing


sol = Solution()

ll = llutils.build_linked_list([1, 2, 3, 4, 5])
assert llutils.get_list_values(sol.reverseList(ll)) == [5, 4, 3, 2, 1]

ll = llutils.build_linked_list([1])
assert llutils.get_list_values(sol.reverseList(ll)) == [1]

ll = llutils.build_linked_list([])
assert llutils.get_list_values(sol.reverseList(ll)) == []

ll = llutils.build_linked_list([1, 2])
assert llutils.get_list_values(sol.reverseList(ll)) == [2, 1]

ll = llutils.build_linked_list([1, 2, 3])
assert llutils.get_list_values(sol.reverseList(ll)) == [3, 2, 1]

ll = llutils.build_linked_list([1, 2, 3, 4])
assert llutils.get_list_values(sol.reverseList(ll)) == [4, 3, 2, 1]

ll = llutils.build_linked_list([-1, 0, 1, 2])
assert llutils.get_list_values(sol.reverseList(ll)) == [2, 1, 0, -1]

ll = llutils.build_linked_list([5, 5, 5])
assert llutils.get_list_values(sol.reverseList(ll)) == [5, 5, 5]

ll = llutils.build_linked_list([-5000])
assert llutils.get_list_values(sol.reverseList(ll)) == [-5000]

ll = llutils.build_linked_list([0, 0])
assert llutils.get_list_values(sol.reverseList(ll)) == [0, 0]
