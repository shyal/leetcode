"""
DRILL: Reverse Sublist

Given the head h of a linked list, reverse the list in place. Return the
new head and the new tail, in that order. The new tail is the node that
was h.

Example 1:

Input: h = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1], tail 1

Example 2:

Input: h = [1, 2]
Output: [2, 1], tail 1

Example 3:

Input: h = [7]
Output: [7], tail 7

Constraints:

    1 <= number of nodes <= 5000
    -5000 <= Node.val <= 5000

    REQUIRED: O(n) time, O(1) extra space, pointers flipped in place. NO
    list of nodes, NO recursion, NO writing to val.
"""


class Solution:
    def reverseSublist(self, h: ListNode) -> Tuple[ListNode, ListNode]:
        pass


sol = Solution()

h = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(h)
head, tail = sol.reverseSublist(h)
print(get_list_values(head), tail.val)  # [5, 4, 3, 2, 1] 1


def rev(vals):
    head, tail = sol.reverseSublist(build_linked_list(vals))
    return get_list_values(head), tail.val, tail.next


# assert rev([1, 2, 3, 4, 5]) == ([5, 4, 3, 2, 1], 1, None)
# assert rev([1, 2]) == ([2, 1], 1, None)
# assert rev([7]) == ([7], 7, None)
# assert rev([3, 3, 3]) == ([3, 3, 3], 3, None)
# assert rev([-5000, 5000]) == ([5000, -5000], -5000, None)
# assert rev(list(range(5000))) == (list(range(4999, -1, -1)), 0, None)
