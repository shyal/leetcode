"""
URL: https://leetcode.com/problems/odd-even-linked-list/description/

328. Odd Even Linked List

Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the regrouped list.

The first node is considered odd, and the second node is even, and so on.

Note that the relative order inside both the even and odd groups should remain as it was in the input.

You must solve the problem in O(1) extra space complexity and O(n) time complexity.

Example 1:

Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]

Example 2:

Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]

Constraints:

    The number of nodes in the linked list is in the range [0, 10^4].
    -10^6 <= Node.val <= 10^6

"""


class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return
        do = ListNode("dh", head)
        de = ListNode("de", head.next)
        a = head
        b = head.next
        while a and b and b.next:
            a.next = b.next
            b.next = b.next.next
            a = a.next
            b = b.next
        a.next = de.next
        return do.next


sol = Solution()

ll = build_linked_list([1, 2, 3, 4, 5])
draw_linked_list(ll)
# print(get_list_values(sol.oddEvenList(ll)))  # [1,3,5,2,4]

assert get_list_values(sol.oddEvenList(build_linked_list([1, 2, 3, 4, 5]))) == [
    1,
    3,
    5,
    2,
    4,
]
assert get_list_values(sol.oddEvenList(build_linked_list([2, 1, 3, 5, 6, 4, 7]))) == [
    2,
    3,
    6,
    7,
    1,
    5,
    4,
]
assert get_list_values(sol.oddEvenList(build_linked_list([]))) == []
assert get_list_values(sol.oddEvenList(build_linked_list([1]))) == [1]
assert get_list_values(sol.oddEvenList(build_linked_list([1, 2]))) == [1, 2]
assert get_list_values(sol.oddEvenList(build_linked_list([1, 2, 3]))) == [1, 3, 2]
assert get_list_values(sol.oddEvenList(build_linked_list([1, 2, 3, 4]))) == [1, 3, 2, 4]
assert get_list_values(
    sol.oddEvenList(build_linked_list([2, 1, 3, 5, 6, 4, 7, 8]))
) == [2, 3, 6, 7, 1, 5, 4, 8]
assert get_list_values(sol.oddEvenList(build_linked_list([-1, 2, -3, 4]))) == [
    -1,
    -3,
    2,
    4,
]
assert get_list_values(sol.oddEvenList(build_linked_list([0]))) == [0]
assert get_list_values(sol.oddEvenList(build_linked_list([0, 0]))) == [0, 0]
assert get_list_values(sol.oddEvenList(build_linked_list([1000000, -1000000]))) == [
    1000000,
    -1000000,
]
