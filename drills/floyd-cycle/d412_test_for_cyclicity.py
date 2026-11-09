"""
EPI 7.3 Test for cyclicity

Given the head of a linked list, return the first node of its cycle, or
None when the list has no cycle. The first node of the cycle is the
node on the cycle that is closest to head. The list may be empty.
Use Floyd's cycle-finding algorithm.

Example 1:

Input: head = [1, 2, 3, 4, 5], and the tail 5 links back to the node 3
Output: the node 3
Explanation:

    1 -> 2 -> 3 -> 4 -> 5
              ^         |
              +---------+

Example 2:

Input: head = [1, 2, 3], and the tail 3 links to None
Output: None

Example 3:

Input: head = [7], and the node 7 links to itself
Output: the node 7

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO set or dict of nodes, NO
    changes to the list.
"""


class Solution:
    def has_cycle(self, head: ListNode | None) -> ListNode | None:
        pass


sol = Solution()


def cycle_list(vals, pos):
    """The list of vals, with its tail linked to the node at index pos (-1: None)."""
    head = build_linked_list(vals)
    nodes, it = [], head
    while it:
        nodes.append(it)
        it = it.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return head, nodes


def start(vals, pos):
    """The index of the node has_cycle returns, or None."""
    head, nodes = cycle_list(vals, pos)
    links = [n.next for n in nodes]
    got = sol.has_cycle(head)
    assert [n.next for n in nodes] == links, "the list must not change"
    return None if got is None else nodes.index(got)


head, nodes = cycle_list([1, 2, 3, 4, 5], 2)
got = sol.has_cycle(head)
print(got and got.val)  # 3

# assert start([1, 2, 3, 4, 5], 2) == 2
# assert start([1, 2, 3], -1) is None
# assert start([7], 0) == 0
# assert start([7], -1) is None
# assert start([], -1) is None
# assert start([1, 2], 0) == 0
# assert start([1, 2], 1) == 1
# assert start([1, 2], -1) is None
# assert start([1, 2, 3, 4, 5], 0) == 0
# assert start([1, 2, 3, 4, 5], 4) == 4
# assert start([1, 2, 3, 4, 5, 6], 3) == 3
# assert start([5, 5, 5, 5], 1) == 1
# assert start(list(range(10 ** 5)), -1) is None
# assert start(list(range(10 ** 5)), 0) == 0
# assert start(list(range(10 ** 5)), 10 ** 5 - 1) == 10 ** 5 - 1
# assert start(list(range(10 ** 5)), 31415) == 31415
