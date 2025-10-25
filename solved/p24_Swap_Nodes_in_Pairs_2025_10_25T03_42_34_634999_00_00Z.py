"""
URL: https://leetcode.com/problems/swap-nodes-in-pairs/description/

24. Swap Nodes in Pairs

Given the head of a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)


Example 1:

Input: head = [1,2,3,4]
Output: [2,1,4,3]

Example 2:

Input: head = []
Output: []

Example 3:

Input: head = [1]
Output: [1]


Constraints:

    The number of nodes in the list is in the range [0, 100].
    0 <= Node.val <= 100
"""


class Solution:

    def swapPairs(self, head: ListNode) -> ListNode:
        if head is None or head.next is None:
            return head
        tmp = head.next.next
        new_head = head.next
        new_head.next = head
        head.next = tmp
        if tmp:
            head.next = self.swapPairs(tmp)
        return new_head


sol = Solution()
assert get_list_values(sol.swapPairs(build_linked_list([]))) == []
assert get_list_values(sol.swapPairs(build_linked_list([1]))) == [1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3]))) == [2, 1, 3]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4, 5]))) == [
    2,
    1,
    4,
    3,
    5,
]
assert get_list_values(sol.swapPairs(build_linked_list([0, 0, 0]))) == [0, 0, 0]
assert get_list_values(sol.swapPairs(build_linked_list([100, 0, 100, 0]))) == [
    0,
    100,
    0,
    100,
]
