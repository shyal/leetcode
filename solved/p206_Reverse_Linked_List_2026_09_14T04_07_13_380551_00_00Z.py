"""
URL: https://leetcode.com/problems/reverse-linked-list/description/?envType=problem-list-v2&envId=vn57k9wr

206. Reverse Linked List

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:

Input: head = [1,2]
Output: [2,1]

Example 3:

Input: head = []
Output: []

Constraints:

    The number of nodes in the list is the range [0, 5000].
    -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?

---

I have a mnemonic for this, that i keep forgetting:

don't hunt him = him don't hunt
don't try

I did need to ask for the mnemonic. So this is hinted.

LEETCODE: Accepted (0 ms, 20.5 MB)
"""


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def reverse_sublist(h):
            d = ListNode()
            t = h
            while h:
                # don't hunt him = him don't hunt
                d.next, h.next, h = h, d.next, h.next
            # don't try
            return d.next, t

        head, tail = reverse_sublist(head)
        return head


sol = Solution()

head = build_linked_list([1, 2, 3, 4, 5])
print(head)

print(get_list_values(sol.reverseList(head)))  # [5,4,3,2,1]

assert get_list_values(sol.reverseList(build_linked_list([1, 2, 3, 4, 5]))) == [
    5,
    4,
    3,
    2,
    1,
]
assert get_list_values(sol.reverseList(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.reverseList(build_linked_list([]))) == []

assert get_list_values(sol.reverseList(build_linked_list([0]))) == [0]
assert get_list_values(sol.reverseList(build_linked_list([-1, -2, -3, -4, -5]))) == [
    -5,
    -4,
    -3,
    -2,
    -1,
]
assert get_list_values(sol.reverseList(build_linked_list([5, 5, 5, 5, 5]))) == [
    5,
    5,
    5,
    5,
    5,
]
assert get_list_values(sol.reverseList(build_linked_list([1, 2, 3, 2, 1]))) == [
    1,
    2,
    3,
    2,
    1,
]
assert get_list_values(
    sol.reverseList(build_linked_list([5000, -5000, 0, 5000, -5000]))
) == [-5000, 5000, 0, -5000, 5000]
assert get_list_values(sol.reverseList(build_linked_list([1]))) == [1]
assert get_list_values(sol.reverseList(build_linked_list([1, 0, -1]))) == [-1, 0, 1]
assert get_list_values(
    sol.reverseList(build_linked_list([2, 2, 2, 3, 3, 3, 1, 1, 1]))
) == [1, 1, 1, 3, 3, 3, 2, 2, 2]
