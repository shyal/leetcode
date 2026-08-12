"""
URL: https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/?envType=problem-list-v2&envId=vn57k9wr

19. Remove Nth Node From End of List

Given the head of a linked list, remove the nth node from the end of the list
and return its head.


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


Follow up: Could you do this in one pass?
"""

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        it = head
        trailing = head
        i = 0
        while it:
            if i > n:
                trailing = trailing.next
            it = it.next
            i += 1
        if i == n:
            head = head.next if head else None
            return head
        trailing.next = trailing.next.next if trailing.next else None
        return head


sol = Solution()

assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1]), 1)) == []
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2]), 1)) == [1]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2]), 2)) == [2]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 5)) == [2, 3, 4, 5]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4, 5]), 1)) == [1, 2, 3, 4]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3]), 2)) == [1, 3]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([7, 7, 7]), 2)) == [7, 7]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([0]), 1)) == []
assert get_list_values(sol.removeNthFromEnd(build_linked_list([0, 100]), 1)) == [0]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([100, 0]), 2)) == [0]
assert get_list_values(sol.removeNthFromEnd(build_linked_list(list(range(30))), 30) ) == list(range(1, 30))
assert get_list_values(sol.removeNthFromEnd(build_linked_list(list(range(30))), 1)) == list(range(29))
assert get_list_values(sol.removeNthFromEnd(build_linked_list(list(range(30))), 15)) == list(range(15)) + list(range(16, 30))
assert get_list_values(sol.removeNthFromEnd(build_linked_list([5, 5]), 1)) == [5]
assert get_list_values(sol.removeNthFromEnd(build_linked_list([1, 2, 3, 4]), 3)) == [1, 3, 4]