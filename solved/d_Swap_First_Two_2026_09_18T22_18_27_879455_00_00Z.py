"""
DRILL: Swap First Two

Given the head of a linked list, swap the first two nodes and return the
new head. A list with fewer than two nodes is returned unchanged. The
nodes move; their val fields do not.

Example 1:

Input: head = [1, 2, 3, 4]
Output: [2, 1, 3, 4]

Example 2:

Input: head = [1, 2]
Output: [2, 1]

Example 3:

Input: head = [1]
Output: [1]

Constraints:

    0 <= number of nodes <= 100
    0 <= Node.val <= 100

    REQUIRED: O(1) extra space, relink the two nodes in place. NO copying
    nodes into a list, NO writing to val.

---

Only remembered thanks to mnemonic.

One has to store head.next in a temp variable.

"""


class Solution:
    def swapFirstTwo(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        m, c = head, head.next
        m.next, c.next = c.next, m
        return c


sol = Solution()

head = build_linked_list([1, 2, 3, 4])
draw_linked_list(head)
print(get_list_values(sol.swapFirstTwo(head)))  # [2, 1, 3, 4]

# assert get_list_values(sol.swapFirstTwo(build_linked_list([1, 2, 3, 4]))) == [2, 1, 3, 4]
# assert get_list_values(sol.swapFirstTwo(build_linked_list([1, 2]))) == [2, 1]
# assert get_list_values(sol.swapFirstTwo(build_linked_list([1]))) == [1]
# assert get_list_values(sol.swapFirstTwo(build_linked_list([]))) == []
# assert get_list_values(sol.swapFirstTwo(build_linked_list([1, 2, 3]))) == [2, 1, 3]
# assert get_list_values(sol.swapFirstTwo(build_linked_list([5, 5, 5]))) == [5, 5, 5]
# assert get_list_values(sol.swapFirstTwo(build_linked_list(list(range(100))))) == [1, 0] + list(range(2, 100))
