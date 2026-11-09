"""
EPI 7.10 Implement even-odd merge

Given the head L of a linked list, relink its nodes so that the nodes
at even positions come first and the nodes at odd positions come after
them, and return the head. Positions start at 0. Each group keeps the
order it has in L. The list may be empty.

Example 1:

Input: L = [10, 11, 12, 13, 14]
Output: [10, 12, 14, 11, 13]
Explanation: the nodes 10, 12, 14 are at the positions 0, 2, 4.

Example 2:

Input: L = [7, 8]
Output: [7, 8]

Example 3:

Input: L = []
Output: []

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO list of nodes, NO list of
    values, NO writing to val.
"""


class Solution:
    def even_odd_merge(self, L: ListNode | None) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.even_odd_merge(build_linked_list([10, 11, 12, 13, 14]))))  # [10, 12, 14, 11, 13]


def nodes(h):
    out, seen = [], set()
    while h and id(h) not in seen:
        seen.add(id(h))
        out.append(h)
        h = h.next
    return out


def merge(vals):
    old = nodes(build_linked_list(vals))
    head = sol.even_odd_merge(old[0] if old else None)
    got, want = nodes(head), old[0::2] + old[1::2]
    assert len(got) == len(want) and all(g is w for g, w in zip(got, want)), "relink the nodes"
    assert not got or got[-1].next is None, "the tail must link to None"
    return get_list_values(head)


# assert merge([10, 11, 12, 13, 14]) == [10, 12, 14, 11, 13]
# assert merge([7, 8]) == [7, 8]
# assert merge([]) == []
# assert merge([7]) == [7]
# assert merge([1, 2, 3]) == [1, 3, 2]
# assert merge([1, 2, 3, 4]) == [1, 3, 2, 4]
# assert merge([0, 1, 2, 3, 4, 5]) == [0, 2, 4, 1, 3, 5]
# assert merge([5, 5, 6, 6]) == [5, 6, 5, 6]
# assert merge([9, 8, 7, 6, 5, 4, 3]) == [9, 7, 5, 3, 8, 6, 4]
# assert merge(list(range(10 ** 5))) == list(range(0, 10 ** 5, 2)) + list(range(1, 10 ** 5, 2))
# assert merge(list(range(10 ** 5 - 1))) == list(range(0, 10 ** 5 - 1, 2)) + list(range(1, 10 ** 5 - 1, 2))
