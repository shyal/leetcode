"""
DRILL: Cut At The Middle

Given the head of a linked list with at least two nodes, cut it into two
lists and return their heads as a pair (first, second). The first list
holds the first half of the nodes; when the length is odd the first list
holds the extra node. After the cut the last node of the first list has
next equal to None.

Example 1:

Input: head = [1, 2, 3, 4]
Output: ([1, 2], [3, 4])

Example 2:

Input: head = [1, 2, 3, 4, 5]
Output: ([1, 2, 3], [4, 5])
Explanation: five nodes, so the first list keeps three.

Example 3:

Input: head = [1, 2]
Output: ([1], [2])

Constraints:

    2 <= number of nodes <= 5 * 10**4
    1 <= Node.val <= 1000

    REQUIRED: one pass, O(1) extra space. NO counting the length first,
    NO second walk.
"""


class Solution:
    def cutAtTheMiddle(self, head: ListNode) -> tuple[ListNode, ListNode]:
        fast, slow = head, head
        while fast and fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        first = head
        second = slow.next
        slow.next = None
        return first, second


sol = Solution()

head = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(head)
first, second = sol.cutAtTheMiddle(head)
print(get_list_values(first), get_list_values(second))  # [1, 2, 3] [4, 5]


def cut(vals):
    first, second = sol.cutAtTheMiddle(build_linked_list(vals))
    return get_list_values(first), get_list_values(second)


assert cut([1, 2, 3, 4]) == ([1, 2], [3, 4])
assert cut([1, 2, 3, 4, 5]) == ([1, 2, 3], [4, 5])
assert cut([1, 2]) == ([1], [2])
assert cut([1, 2, 3]) == ([1, 2], [3])
assert cut([7, 7, 7, 7, 7, 7]) == ([7, 7, 7], [7, 7, 7])
assert cut(list(range(1, 11))) == ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
assert cut(list(range(1, 50001))) == (list(range(1, 25001)), list(range(25001, 50001)))
