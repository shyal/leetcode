"""
URL: https://leetcode.com/problems/reorder-list/description/?envType=problem-list-v2&envId=vn57k9wr

143. Reorder List

You are given the head of a singly linked-list. The list can be represented as:

L0 → L1 → … → Ln-1 → Ln
Reorder the list to be on the following form:

L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Example 1:

Input: head = [1,2,3,4]
Output: [1,4,2,3]

Example 2:

Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]

Constraints:

    The number of nodes in the list is in the range [1, 5 * 10^4].
    1 <= Node.val <= 1000


"""


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        it = head
        length = 0
        while it:
            it = it.next
            length += 1

        it = head
        for _ in range(length // 2 + (-1 if length % 2 == 0 else 0)):
            it = it.next

        second_half = it.next
        it.next = None

        d = ListNode(-1)
        h = second_half
        while h:
            d.next, h.next, h = h, d.next, h.next

        second_half = d.next
        d.next = None

        draw_linked_list(head)
        draw_linked_list(second_half)

        it = d

        it1 = head
        it2 = second_half
        i = 0
        while it1 or it2:
            if i % 2 == 0 and it1:
                it.next = it1
                it = it1
                it1 = it1.next
            elif i % 2 != 0 and it2:
                it.next = it2
                it = it2
                it2 = it2.next
            else:
                it.next = (it1 or it2).next
                it = it1 or it2
                it1 = it1.next if it1 else None
                it2 = it2.next if it2 else None
            i += 1

        draw_linked_list(d.next)
        # print("---")

        return d.next


sol = Solution()

head = build_linked_list([1, 2, 3, 4])
sol.reorderList(head)
# head = build_linked_list([1, 2, 3, 4, 5])
# sol.reorderList(head)
# print(get_list_values(head))
assert get_list_values(head) == [1, 4, 2, 3]

head = build_linked_list([1, 2, 3, 4, 5])
sol.reorderList(head)
assert get_list_values(head) == [1, 5, 2, 4, 3]

head = build_linked_list([1])
sol.reorderList(head)
assert get_list_values(head) == [1]

head = build_linked_list([1, 2])
sol.reorderList(head)
assert get_list_values(head) == [1, 2]

head = build_linked_list([1, 2, 3])
sol.reorderList(head)
assert get_list_values(head) == [1, 3, 2]

head = build_linked_list([1, 2, 3, 4, 5, 6])
sol.reorderList(head)
assert get_list_values(head) == [1, 6, 2, 5, 3, 4]

head = build_linked_list([5, 4, 3, 2, 1])
sol.reorderList(head)
assert get_list_values(head) == [5, 1, 4, 2, 3]
