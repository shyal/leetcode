"""
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

83. Remove Duplicates from Sorted List

Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.

Example 1:

Input: head = [1,1,2]
Output: [1,2]

Example 2:

Input: head = [1,1,2,3,3]
Output: [1,2,3]

Constraints:

    The number of nodes in the list is in the range [0, 300].
    -100 <= Node.val <= 100
    The list is guaranteed to be sorted in ascending order.
"""


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dh = ListNode()
        dh.next = head
        it = head
        while it and it.next:
            if it.next.val == it.val:
                it.next = it.next.next
            else:
                it = it.next
        return dh.next


sol = Solution()

ll = build_linked_list([1, 1, 2])
draw_linked_list(ll)
# print(get_list_values(sol.deleteDuplicates(ll)))  # [1,2]

assert get_list_values(sol.deleteDuplicates(build_linked_list([1, 1, 2]))) == [1, 2]
assert get_list_values(sol.deleteDuplicates(build_linked_list([1, 1, 2, 3, 3]))) == [
    1,
    2,
    3,
]
assert get_list_values(sol.deleteDuplicates(build_linked_list([]))) == []
assert get_list_values(sol.deleteDuplicates(build_linked_list([42]))) == [42]
assert get_list_values(sol.deleteDuplicates(build_linked_list([1, 1, 1, 1]))) == [1]
assert get_list_values(sol.deleteDuplicates(build_linked_list([1, 2, 3, 4]))) == [
    1,
    2,
    3,
    4,
]
assert get_list_values(
    sol.deleteDuplicates(build_linked_list([-100, -100, 0, 100, 100]))
) == [-100, 0, 100]
assert get_list_values(sol.deleteDuplicates(build_linked_list([1, 2, 2, 3, 3, 4]))) == [
    1,
    2,
    3,
    4,
]
assert get_list_values(sol.deleteDuplicates(build_linked_list([-5, -5, -5]))) == [-5]
assert get_list_values(sol.deleteDuplicates(build_linked_list([0]))) == [0]
