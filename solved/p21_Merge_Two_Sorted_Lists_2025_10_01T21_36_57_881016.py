"""
URL: https://leetcode.com/problems/merge-two-sorted-lists/description/

21. Merge Two Sorted Lists

You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.


Example 1:

Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:

Input: list1 = [], list2 = []
Output: []

Example 3:

Input: list1 = [], list2 = [0]
Output: [0]


Constraints:

        The number of nodes in both lists is in the range [0, 50].
        -100 <= Node.val <= 100
        Both list1 and list2 are sorted in non-decreasing order.
"""


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        l1 = list1
        l2 = list2

        def pop(L):
            if L:
                next = L.next
                L.next = None
                return L, next
            return None, None

        def pop_smallest(l1, l2):
            if l1 and l2:
                if l1.val < l2.val:
                    popped, new_l1 = pop(l1)
                    return popped, new_l1, l2
                else:
                    popped, new_l2 = pop(l2)
                    return popped, l1, new_l2
            else:
                l = l1 or l2
                popped, new = pop(l)
                return popped, new, None

        it = ListNode(-1)
        dummy_head = it
        while it:
            popped, l1, l2 = pop_smallest(l1, l2)
            it.next = popped
            it = it.next
        return dummy_head.next


sol = Solution()
list1 = build_linked_list([1, 2, 4])
list2 = build_linked_list([1, 3, 4])
# draw_linked_list(list1)
# draw_linked_list(list2)
res = sol.mergeTwoLists(list1, list2)
assert get_list_values(sol.mergeTwoLists(list1, list2)) == [1, 1, 2, 3, 4, 4]

sol = Solution()
list1 = build_linked_list([])
list2 = build_linked_list([])
# draw_linked_list(list1)
# draw_linked_list(list2)
assert get_list_values(sol.mergeTwoLists(list1, list2)) == []

sol = Solution()
list1 = build_linked_list([])
list2 = build_linked_list([0])
# draw_linked_list(list1)
# draw_linked_list(list2)
assert get_list_values(sol.mergeTwoLists(list1, list2)) == [0]
