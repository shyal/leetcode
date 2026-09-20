"""
DRILL: Remove Value

Given the head of a linked list and an integer val, remove every node
whose value is val and return the head of what remains. The removed
nodes may be at the head, in the middle, at the tail, or everywhere.

Example 1:

Input: head = [1, 2, 6, 3, 4, 5, 6], val = 6
Output: [1, 2, 3, 4, 5]

Example 2:

Input: head = [7, 7, 7, 7], val = 7
Output: []

Example 3:

Input: head = [7, 1, 7, 2], val = 7
Output: [1, 2]

Constraints:

    0 <= number of nodes <= 10**4
    1 <= Node.val <= 50
    1 <= val <= 50

    REQUIRED: one pass, O(1) extra space, one loop with NO special case
    for the head. NO list of values, NO second list.

---

Learning

"""


class Solution:
    def removeValue(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        d = pre = ListNode(0, head)
        while pre.next:
            if pre.next.val == val:
                pre.next = pre.next.next
            else:
                pre = pre.next
        return d.next


sol = Solution()

head = build_linked_list([7, 1, 7, 2])
draw_linked_list(head)
print(get_list_values(sol.removeValue(head, 7)))  # [1, 2]


def rm(vals, val):
    return get_list_values(sol.removeValue(build_linked_list(vals), val))


# assert rm([1, 2, 6, 3, 4, 5, 6], 6) == [1, 2, 3, 4, 5]
# assert rm([7, 7, 7, 7], 7) == []
# assert rm([7, 1, 7, 2], 7) == [1, 2]
# assert rm([], 1) == []
# assert rm([1], 1) == []
# assert rm([1], 2) == [1]
# assert rm([1, 2, 3], 2) == [1, 3]
# assert rm([1, 2, 3], 3) == [1, 2]
# assert rm([2, 2, 1, 2, 2], 2) == [1]
# assert rm([1, 2] * 5000, 2) == [1] * 5000
