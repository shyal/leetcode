"""
EPI 9.15 Compute the right sibling tree

Given tree, the root of a perfect binary tree, set the field next of every
node to the node on its right in the same level, or to None when the node
is the last in its level. A perfect binary tree has all its leaves at the
same depth, and every other node has two children. Change the tree in
place and return None.

Example 1:

Input: tree = [1, 2, 3, 4, 5, 6, 7]
Output: None. The next fields link 2 to 3, and 4 to 5 to 6 to 7.

          1
        /   \\
       2     3
      / \\   / \\
     4   5 6   7

Example 2:

Input: tree = [1]
Output: None. The next field of 1 is None.

Example 3:

Input: tree = []
Output: None

Constraints:

    0 <= number of nodes <= 2^16 - 1
    The tree is a perfect binary tree.

    REQUIRED: O(n) time for n nodes, O(1) extra space. NO queue. NO
    recursion.
"""


class Solution:
    def construct_right_sibling(self, tree: TreeNode | None) -> None:
        pass


sol = Solution()


def next_chains(root: TreeNode | None) -> list[list[int]]:
    chains = []
    while root:
        chain, node = [], root
        while node:
            chain.append(node.val)
            node = getattr(node, "next", None)
        chains.append(chain)
        root = root.left
    return chains


t = build_tree([1, 2, 3, 4, 5, 6, 7])
draw_tree(t)
sol.construct_right_sibling(t)
print(next_chains(t))  # [[1], [2, 3], [4, 5, 6, 7]]

# t = build_tree([1, 2, 3, 4, 5, 6, 7])
# assert sol.construct_right_sibling(t) is None
# assert next_chains(t) == [[1], [2, 3], [4, 5, 6, 7]]
# assert hasattr(t, "next") and t.next is None
# assert find_node(t, 3).next is None and find_node(t, 7).next is None
# assert find_node(t, 5).next is find_node(t, 6)
# t = build_tree([1])
# sol.construct_right_sibling(t)
# assert next_chains(t) == [[1]]
# assert hasattr(t, "next") and t.next is None
# sol.construct_right_sibling(None)
# assert next_chains(None) == []
# t = build_tree([1, 2, 3])
# sol.construct_right_sibling(t)
# assert next_chains(t) == [[1], [2, 3]]
# assert find_node(t, 3).next is None
# t = build_tree([0] * 15)
# sol.construct_right_sibling(t)
# assert [len(c) for c in next_chains(t)] == [1, 2, 4, 8]
# t = build_tree(list(range(2 ** 16 - 1)))
# sol.construct_right_sibling(t)
# assert next_chains(t) == [list(range(2 ** d - 1, 2 ** (d + 1) - 1)) for d in range(16)]
