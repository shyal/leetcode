"""
EPI 7.4 Test for overlapping lists - lists are cycle-free

Given the heads l0 and l1 of two linked lists with no cycle, return the
first node that is in both lists, or None when no node is in both. Two
lists that share a node share every node after it. Either list may be
empty.

Example 1:

Input: l0 = [1, 2, 3, 7, 8, 9], l1 = [4, 5, 7, 8, 9], and the nodes
7, 8, 9 are the same nodes in both lists
Output: the node 7
Explanation:

    l0:  1 -> 2 -> 3 -+
                      |
                      +-> 7 -> 8 -> 9
                      |
    l1:       4 -> 5 -+

Example 2:

Input: l0 = [1, 2], l1 = [3, 4], and no node is in both lists
Output: None

Example 3:

Input: l0 = [6, 7], l1 = [5, 6, 7], and the nodes 6, 7 are the same
nodes in both lists
Output: the node 6
Explanation: the head of l0 is in l1.

Constraints:

    0 <= number of nodes in l0, l1 <= 10^5
    The lists have no cycle.

    REQUIRED: O(n + m) time, O(1) extra space. NO set or dict of nodes,
    NO changes to the lists.
"""


class Solution:
    def overlapping_no_cycle_lists(
        self, l0: ListNode | None, l1: ListNode | None
    ) -> ListNode | None:
        pass


sol = Solution()


def lists(a, b, c):
    """l0 = a then c, l1 = b then c, where the nodes of c are in both lists."""
    l0, l1, common = build_linked_list(a), build_linked_list(b), build_linked_list(c)
    heads = []
    for h in (l0, l1):
        if h is None:
            heads.append(common)
            continue
        it = h
        while it.next:
            it = it.next
        it.next = common
        heads.append(h)
    return heads[0], heads[1], common


def first_common(a, b, c):
    """The value of the node that overlapping_no_cycle_lists returns, or None.
    The values in a, b and c are distinct."""
    l0, l1, common = lists(a, b, c)
    got = sol.overlapping_no_cycle_lists(l0, l1)
    assert got is common, "return the first node that is in both lists"
    assert get_list_values(l0) == a + c and get_list_values(l1) == b + c, "the lists must not change"
    return None if got is None else got.val


l0, l1, common = lists([1, 2, 3], [4, 5], [7, 8, 9])
got = sol.overlapping_no_cycle_lists(l0, l1)
print(got and got.val)  # 7

# assert first_common([1, 2, 3], [4, 5], [7, 8, 9]) == 7
# assert first_common([1, 2], [3, 4], []) is None
# assert first_common([], [5], [6, 7]) == 6
# assert first_common([5], [], [6, 7]) == 6
# assert first_common([], [], [6, 7]) == 6
# assert first_common([], [], []) is None
# assert first_common([1], [], []) is None
# assert first_common([], [1], []) is None
# assert first_common([1], [2], [3]) == 3
# assert first_common([1, 2, 3, 4], [5], [6]) == 6
# assert first_common([5], [1, 2, 3, 4], [6]) == 6
# assert first_common([1, 2, 3, 4], [5, 6, 7, 8], [9]) == 9
# assert first_common([1, 2, 3], [4, 5, 6], []) is None
# assert first_common(list(range(10 ** 5 - 1)), [-1], [10 ** 5]) == 10 ** 5
# assert first_common([-1], list(range(5 * 10 ** 4)), list(range(5 * 10 ** 4, 10 ** 5))) == 5 * 10 ** 4
# assert first_common(list(range(5 * 10 ** 4)), list(range(5 * 10 ** 4, 10 ** 5)), []) is None
