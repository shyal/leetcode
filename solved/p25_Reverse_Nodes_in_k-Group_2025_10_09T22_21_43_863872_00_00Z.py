"""
URL: https://leetcode.com/problems/reverse-nodes-in-k-group/description/

25. Reverse Nodes in k-Group

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

Example 1:

Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]

Example 2:

Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]

Constraints:

    The number of nodes in the list is n.
    1 <= k <= n <= 5000
    0 <= Node.val <= 1000
"""


class Solution:
    def reverse_sublist(self, h, n):
        d = ListNode(-1)
        t = h
        for _ in range(n):
            if not h:
                break
            d.next, h.next, h = h, d.next, h.next
        else:
            t.next = h
        return d.next, t

    def get_length(self, h, c=0):
        while h:
            h, c = h.next, c + 1
        return c

    def reverseKGroup(self, h: Optional[ListNode], k: int) -> Optional[ListNode]:
        it = d = ListNode(-1, h)
        n = self.get_length(h)
        for _ in range(n // k):
            it.next, it = self.reverse_sublist(it.next, k)
        return d.next


sol = Solution()

# print(
#     get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5]), 2))
# )  # [2,1,4,3,5]

assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5]), 2)) == [
    2,
    1,
    4,
    3,
    5,
]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5]), 3)) == [
    3,
    2,
    1,
    4,
    5,
]
assert get_list_values(sol.reverseKGroup(build_linked_list([1]), 1)) == [1]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2]), 1)) == [1, 2]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2]), 2)) == [2, 1]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3]), 2)) == [2, 1, 3]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3]), 3)) == [3, 2, 1]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4]), 2)) == [
    2,
    1,
    4,
    3,
]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5]), 5)) == [
    5,
    4,
    3,
    2,
    1,
]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5]), 1)) == [
    1,
    2,
    3,
    4,
    5,
]
assert get_list_values(sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5, 6]), 3)) == [
    3,
    2,
    1,
    6,
    5,
    4,
]
assert get_list_values(
    sol.reverseKGroup(build_linked_list([1, 2, 3, 4, 5, 6, 7]), 3)
) == [3, 2, 1, 6, 5, 4, 7]
assert get_list_values(sol.reverseKGroup(build_linked_list([]), 1)) == []
