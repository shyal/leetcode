"""
EPI 7.2 Reverse a single sublist

Given the head L of a linked list and two positions start and finish,
reverse the order of the nodes from position start to position finish,
both included, and return the head of the list. Positions start at 1.
The nodes move; their values do not change.

Example 1:

Input: L = [11, 3, 5, 7, 2], start = 2, finish = 4
Output: [11, 7, 5, 3, 2]

Example 2:

Input: L = [1, 2, 3], start = 1, finish = 3
Output: [3, 2, 1]

Example 3:

Input: L = [1, 2, 3], start = 2, finish = 2
Output: [1, 2, 3]

Constraints:

    1 <= n <= 10^5, where n is the number of nodes in L
    1 <= start <= finish <= n
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO list of nodes, NO writing
    to val, NO recursion.
"""


class Solution:
    def reverse_sublist(self, L: ListNode, start: int, finish: int) -> ListNode:
        pass


sol = Solution()

print(get_list_values(sol.reverse_sublist(build_linked_list([11, 3, 5, 7, 2]), 2, 4)))  # [11, 7, 5, 3, 2]


def nodes(h):
    out = []
    while h:
        out.append(h)
        h = h.next
    return out


def rev(vals, start, finish):
    old = nodes(build_linked_list(vals))
    head = sol.reverse_sublist(old[0], start, finish)
    want = old[: start - 1] + old[start - 1 : finish][::-1] + old[finish:]
    got = nodes(head)
    assert len(got) == len(want) and all(g is w for g, w in zip(got, want)), "relink the nodes"
    return get_list_values(head)


# assert rev([11, 3, 5, 7, 2], 2, 4) == [11, 7, 5, 3, 2]
# assert rev([1, 2, 3], 1, 3) == [3, 2, 1]
# assert rev([1, 2, 3], 2, 2) == [1, 2, 3]
# assert rev([7], 1, 1) == [7]
# assert rev([1, 2], 1, 2) == [2, 1]
# assert rev([1, 2], 1, 1) == [1, 2]
# assert rev([1, 2], 2, 2) == [1, 2]
# assert rev([1, 2, 3, 4, 5], 1, 3) == [3, 2, 1, 4, 5]
# assert rev([1, 2, 3, 4, 5], 3, 5) == [1, 2, 5, 4, 3]
# assert rev([1, 2, 3, 4, 5], 4, 5) == [1, 2, 3, 5, 4]
# assert rev([1, 2, 3, 4, 5], 1, 5) == [5, 4, 3, 2, 1]
# assert rev([3, 3, 1, 3], 2, 3) == [3, 1, 3, 3]
# assert rev(list(range(10 ** 5)), 1, 10 ** 5) == list(range(10 ** 5 - 1, -1, -1))
# assert rev(list(range(10 ** 5)), 2, 10 ** 5 - 1) == [0] + list(range(10 ** 5 - 2, 0, -1)) + [10 ** 5 - 1]
