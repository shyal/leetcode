"""
EPI 7.5 Test for overlapping lists - lists may have cycles

Given the heads l0 and l1 of two linked lists, where each list may have
a cycle, return a node that is in both lists, or None when no node is in
both. A node is in a list when a walk from the head reaches it. Any node
that is in both lists is a correct answer. Either list may be empty.

Example 1:

Input: l0 = 1 -> 2 -> 3 -> 4 -> 5 -> back to 3, l1 = 6 -> the node 2
Output: the node 2, 3, 4 or 5
Explanation:

    l0:  1 -+
            +-> 2 -> 3 -> 4 -> 5
    l1:  6 -+        ^         |
                     +---------+

Example 2:

Input: l0 = 1 -> 2 -> 3 -> back to 2, l1 = 4 -> the node 3
Output: the node 2 or 3
Explanation: l1 enters the cycle of l0 at a different node.

Example 3:

Input: l0 = 1 -> 2 -> 3 -> back to 1, l1 = 4 -> 5 -> None
Output: None

Constraints:

    0 <= number of nodes in l0, l1 <= 10^5

    REQUIRED: O(n + m) time, O(1) extra space. NO set or dict of nodes,
    NO changes to the lists.
"""


class Solution:
    def overlapping_lists(
        self, l0: ListNode | None, l1: ListNode | None
    ) -> ListNode | None:
        pass


sol = Solution()


def build(links):
    """links maps each node value to the value of its next node, or None."""
    nodes = {v: ListNode(v) for v in links}
    for v, w in links.items():
        nodes[v].next = None if w is None else nodes[w]
    return nodes


def meets(links, h0, h1):
    """The value of the node that overlapping_lists returns, or None. The
    heads are the values h0 and h1, and None is an empty list."""
    nodes = build(links)
    before = {v: n.next for v, n in nodes.items()}
    got = sol.overlapping_lists(nodes.get(h0), nodes.get(h1))
    assert all(nodes[v].next is w for v, w in before.items()), "the lists must not change"
    if got is None:
        return None
    assert nodes.get(got.val) is got, "return a node of the lists"
    return got.val


nodes = build({1: 2, 2: 3, 3: 4, 4: 5, 5: 3, 6: 2})
got = sol.overlapping_lists(nodes[1], nodes[6])
print(got and got.val)  # 2, 3, 4 or 5

# assert meets({1: 2, 2: 3, 3: 4, 4: 5, 5: 3, 6: 2}, 1, 6) in {2, 3, 4, 5}
# assert meets({1: 2, 2: 3, 3: 2, 4: 3}, 1, 4) in {2, 3}
# assert meets({1: 2, 2: 3, 3: 1, 4: 5, 5: None}, 1, 4) is None
# assert meets({1: 2, 2: 3, 3: 1, 4: 5, 5: None}, 4, 1) is None
# assert meets({1: 2, 2: 1, 3: 4, 4: 3}, 1, 3) is None
# assert meets({1: 2, 2: 3, 3: None, 4: 2}, 1, 4) in {2, 3}
# assert meets({1: 2, 2: None, 3: None}, 1, 3) is None
# assert meets({1: 2, 2: 1}, 1, 1) in {1, 2}
# assert meets({1: 2, 2: 1}, None, 1) is None
# assert meets({1: None}, 1, None) is None
# assert meets({}, None, None) is None
# assert meets({1: 1, 2: 1}, 2, 1) == 1
# assert meets({1: 3, 2: 3, 3: 4, 4: 3}, 1, 2) in {3, 4}
# assert meets({1: 3, 2: 4, 3: 4, 4: 5, 5: 3}, 1, 2) in {3, 4, 5}
# assert meets({1: 2, 2: 3, 3: 2}, 1, 3) in {2, 3}
# assert meets({1: 2, 2: 3, 3: 4, 4: 2, 5: None}, 1, 5) is None
# assert meets({**{i: (i + 1) % 10 ** 5 for i in range(10 ** 5)}, -1: 5 * 10 ** 4}, 0, -1) in range(10 ** 5)
# assert meets({**{i: (i + 1) % 10 ** 5 for i in range(10 ** 5)}, **{-i: -i - 1 for i in range(1, 10 ** 5)}, -10 ** 5: -1}, 0, -1) is None
# assert meets({**{i: i + 1 for i in range(10 ** 5 - 1)}, 10 ** 5 - 1: None, -1: 10 ** 5 - 1}, 0, -1) == 10 ** 5 - 1
