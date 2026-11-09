"""
EPI 7.9 Implement cyclic right shift for singly linked lists

Given the head L of a linked list and an integer k, shift the list to
the right by k places and return the head. A shift to the right by one
place moves the tail node to the front. The list may be empty.

Example 1:

Input: L = [2, 3, 5, 3, 2], k = 3
Output: [5, 3, 2, 2, 3]

Example 2:

Input: L = [1, 2, 3], k = 4
Output: [3, 1, 2]
Explanation: a shift by 3 places gives the list [1, 2, 3] again.

Example 3:

Input: L = [1, 2, 3], k = 0
Output: [1, 2, 3]

Constraints:

    0 <= n <= 10^5, where n is the number of nodes in L
    0 <= k <= 10^9
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO list of nodes, NO list of
    values, NO new nodes.
"""


class Solution:
    def cyclically_right_shift_list(self, L: ListNode | None, k: int) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.cyclically_right_shift_list(build_linked_list([2, 3, 5, 3, 2]), 3)))  # [5, 3, 2, 2, 3]


def nodes(h):
    out, seen = [], set()
    while h and id(h) not in seen:
        seen.add(id(h))
        out.append(h)
        h = h.next
    return out


def shift(vals, k):
    L = build_linked_list(vals)
    old = nodes(L)
    head = sol.cyclically_right_shift_list(L, k)
    got = nodes(head)
    s = k % len(old) if old else 0
    want = old[len(old) - s :] + old[: len(old) - s]
    assert len(got) == len(want) and all(g is w for g, w in zip(got, want)), "relink the nodes"
    assert not got or got[-1].next is None, "the tail must link to None"
    return get_list_values(head)


# assert shift([2, 3, 5, 3, 2], 3) == [5, 3, 2, 2, 3]
# assert shift([1, 2, 3], 4) == [3, 1, 2]
# assert shift([1, 2, 3], 0) == [1, 2, 3]
# assert shift([1, 2, 3], 3) == [1, 2, 3]
# assert shift([1, 2, 3], 1) == [3, 1, 2]
# assert shift([1, 2, 3], 2) == [2, 3, 1]
# assert shift([], 0) == []
# assert shift([], 5) == []
# assert shift([7], 0) == [7]
# assert shift([7], 10 ** 9) == [7]
# assert shift([1, 2], 1) == [2, 1]
# assert shift([1, 2], 10 ** 9) == [1, 2]
# assert shift([1, 2, 3, 4, 5], 10 ** 9 - 1) == [2, 3, 4, 5, 1]
# assert shift(list(range(10 ** 5)), 1) == [10 ** 5 - 1] + list(range(10 ** 5 - 1))
# assert shift(list(range(10 ** 5)), 10 ** 9 - 10 ** 5 + 1) == [10 ** 5 - 1] + list(range(10 ** 5 - 1))
# assert shift(list(range(10 ** 5)), 10 ** 5 - 1) == list(range(1, 10 ** 5)) + [0]
