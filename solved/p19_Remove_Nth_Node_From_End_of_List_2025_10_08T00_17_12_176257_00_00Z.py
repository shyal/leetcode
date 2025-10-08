"""
URL: https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/

19. Remove Nth Node From End of List

Given the head of a linked list, remove the nth node from the end of the list and return its head.

Example 1:

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]

Example 2:

Input: head = [1], n = 1
Output: []

Example 3:

Input: head = [1,2], n = 1
Output: [1]

Constraints:

    The number of nodes in the list is sz.
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz

---

OK so we'll need to iterate until the end of the list, and maintain a back
pointer, so it points to end -n.


"""


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        it = head
        dummy = ListNode()
        dummy.next = head
        trailing = dummy
        i = 0
        while it:
            if i >= n:
                trailing = trailing.next
            it = it.next
            i += 1
        if trailing:
            trailing.next = trailing.next.next if trailing.next else None
        return dummy.next


sol = Solution()

# ll = build_linked_list([1, 2, 3, 4, 5])
# draw_linked_list(ll)
# res = sol.removeNthFromEnd(ll, 2)
# draw_linked_list(res)  # [1, 2, 3, 5]

assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 2)) == [
    1,
    2,
    3,
    5,
]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1]), 1)) == []
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2]), 1)) == [1]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 1)) == [
    1,
    2,
    3,
    4,
]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 5)) == [
    2,
    3,
    4,
    5,
]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2]), 2)) == [2]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3]), 3)) == [2, 3]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3]), 2)) == [1, 3]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3]), 1)) == [1, 2]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 1, 1]), 2)) == [1, 1]
