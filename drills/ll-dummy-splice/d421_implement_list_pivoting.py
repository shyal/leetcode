"""
EPI 7.12 Implement list pivoting

Given the head l of a linked list and an integer x, relink the nodes so
that the nodes with a value less than x come first, then the nodes with
a value equal to x, then the nodes with a value greater than x, and
return the head. Each of the three groups keeps the order it has in l.
The value x does not have to be in the list.

Example 1:

Input: l = [3, 2, 2, 11, 7, 5, 11], x = 7
Output: [3, 2, 2, 5, 7, 11, 11]

Example 2:

Input: l = [5, 1, 9], x = 4
Output: [1, 5, 9]

Example 3:

Input: l = [], x = 3
Output: []

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= Node.val, x <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO sorting, NO list of nodes,
    NO list of values, NO writing to val.
"""


class Solution:
    def list_pivoting(self, l: ListNode | None, x: int) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.list_pivoting(build_linked_list([3, 2, 2, 11, 7, 5, 11]), 7)))  # [3, 2, 2, 5, 7, 11, 11]


def nodes(h):
    out, seen = [], set()
    while h and id(h) not in seen:
        seen.add(id(h))
        out.append(h)
        h = h.next
    return out


def pivot(vals, x):
    old = nodes(build_linked_list(vals))
    head = sol.list_pivoting(old[0] if old else None, x)
    got = nodes(head)
    want = [n for n in old if n.val < x] + [n for n in old if n.val == x] + [n for n in old if n.val > x]
    assert len(got) == len(want) and all(g is w for g, w in zip(got, want)), "relink the nodes, keep each group in order"
    assert not got or got[-1].next is None, "the tail must link to None"
    return get_list_values(head)


# assert pivot([3, 2, 2, 11, 7, 5, 11], 7) == [3, 2, 2, 5, 7, 11, 11]
# assert pivot([5, 1, 9], 4) == [1, 5, 9]
# assert pivot([], 3) == []
# assert pivot([3], 3) == [3]
# assert pivot([3], 1) == [3]
# assert pivot([3], 5) == [3]
# assert pivot([2, 1], 1) == [1, 2]
# assert pivot([1, 2, 3], 0) == [1, 2, 3]
# assert pivot([1, 2, 3], 4) == [1, 2, 3]
# assert pivot([3, 2, 1], 2) == [1, 2, 3]
# assert pivot([7, 7, 1, 7, 9, 0], 7) == [1, 0, 7, 7, 7, 9]
# assert pivot([9, 8, 7, 6, 5, 4], 6) == [5, 4, 6, 9, 8, 7]
# assert pivot([4, 4, 4], 4) == [4, 4, 4]
# assert pivot(list(range(10 ** 5, 0, -1)), 5 * 10 ** 4) == list(range(5 * 10 ** 4 - 1, 0, -1)) + [5 * 10 ** 4] + list(range(10 ** 5, 5 * 10 ** 4, -1))
# assert pivot([v % 3 for v in range(10 ** 5)], 1) == [0] * 33334 + [1] * 33333 + [2] * 33333
