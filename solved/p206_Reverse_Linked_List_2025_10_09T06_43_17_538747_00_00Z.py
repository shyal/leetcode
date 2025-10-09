"""
URL: https://leetcode.com/problems/reverse-linked-list/description/

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

Ok so this is the best iterative alg, IMO. It's not my solution, i'm just learning here.
We start with a dummy head, not pointing to head. We iterate as long as head is valid.
We use tuple unpacking and perform all the work in one go.

We start with the dummy.next first, and it'll get simultaneously assigned head.
Ultimately we'll return d.next. For now, it performs that first connection, of
making the dummy.next point to the head.

Then we simultaneously connect h.next to d.next, which sets it to None on our first
iteration.

Finally h becomes h.next, which we can really just think of as regular iterating of
an 'it' or 'curr' pointer.

"""


class Solution:
    def reverseList(self, h: Optional[ListNode]) -> Optional[ListNode]:
        # Not my solution. Still learning.
        d = ListNode(0)
        while h:
            d.next, h.next, h = h, d.next, h.next
        return d.next


sol = Solution()

head = build_linked_list([1, 2, 3, 4, 5])
result = sol.reverseList(head)
# print_linked_list(result)  # [5,4,3,2,1]

assert get_list_values(sol.reverseList(build_linked_list([1, 2, 3, 4, 5]))) == [
    5,
    4,
    3,
    2,
    1,
]
assert get_list_values(sol.reverseList(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.reverseList(build_linked_list([]))) == []
assert get_list_values(sol.reverseList(build_linked_list([42]))) == [42]
assert get_list_values(sol.reverseList(build_linked_list([-1, 0, 1]))) == [1, 0, -1]
assert get_list_values(sol.reverseList(build_linked_list([2, 2, 2]))) == [2, 2, 2]
assert get_list_values(sol.reverseList(build_linked_list([5000, -5000]))) == [
    -5000,
    5000,
]
assert get_list_values(sol.reverseList(build_linked_list([0]))) == [0]
