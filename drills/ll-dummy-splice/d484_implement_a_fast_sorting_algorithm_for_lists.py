"""
EPI 13.11 Implement a fast sorting algorithm for lists

Given the head L of a singly linked list of integers, sort the list in
nondecreasing order by relinking its nodes, and return the new head. The
sort must be stable: two nodes with equal values keep their original
order.

Example 1:

Input: L = 3 -> 1 -> 2 -> 1
Output: 1 -> 1 -> 2 -> 3
Explanation: the 1 that came first in L is still first.

Example 2:

Input: L = 5
Output: 5

Example 3:

Input: L = None
Output: None

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= node value <= 10^9

    REQUIRED: O(n log n) time and O(log n) extra space, where n is the
    number of nodes. NO sorted() and NO list.sort().
"""


class Solution:
    def stable_sort_list(self, L: ListNode | None) -> ListNode | None:
        pass


sol = Solution()

head = build_linked_list([3, 1, 2, 1])
draw_linked_list(head)
print(get_list_values(sol.stable_sort_list(head)))  # [1, 1, 2, 3]


def sort_vals(vals):
    return get_list_values(sol.stable_sort_list(build_linked_list(vals)))


# assert sort_vals([3, 1, 2, 1]) == [1, 1, 2, 3]
# assert sort_vals([5]) == [5]
# assert sol.stable_sort_list(None) is None
# assert sort_vals([1, 2]) == [1, 2]
# assert sort_vals([2, 1]) == [1, 2]
# assert sort_vals([4, 4, 4]) == [4, 4, 4]
# assert sort_vals([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
# assert sort_vals([-1, 3, -7, 0, 3, 2]) == [-7, -1, 0, 2, 3, 3]
# d = ListNode(1)
# c = ListNode(2, d)
# b = ListNode(1, c)
# a = ListNode(2, b)
# head = sol.stable_sort_list(a)
# assert head is b and b.next is d and d.next is a and a.next is c and c.next is None
# assert sort_vals(list(range(10 ** 5, 0, -1))) == list(range(1, 10 ** 5 + 1))
# assert sort_vals([i * 7919 % 10007 for i in range(10 ** 5)]) == sorted(i * 7919 % 10007 for i in range(10 ** 5))
# assert sort_vals([i % 3 for i in range(10 ** 5)]) == sorted(i % 3 for i in range(10 ** 5))
