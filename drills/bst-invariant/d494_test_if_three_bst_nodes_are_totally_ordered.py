"""
EPI 14.9 Test if three BST nodes are totally ordered

Given three distinct nodes possible_anc_or_desc_0, possible_anc_or_desc_1
and middle of a binary search tree, return True when one of the first two
nodes is an ancestor of middle and the other is a descendant of middle.
Return False otherwise. Every key in the tree is distinct. The root of
the tree is not given.

Example 1:

Input: tree = [20, 9, 25, 5, 12, None, None, None, None, 11, 14],
       possible_anc_or_desc_0 = the node 20,
       possible_anc_or_desc_1 = the node 11, middle = the node 9
Output: True
Explanation: 20 is an ancestor of 9, and 11 is a descendant of 9.

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: the same tree, possible_anc_or_desc_0 = the node 14,
       possible_anc_or_desc_1 = the node 20, middle = the node 12
Output: True
Explanation: the order of the first two nodes does not matter.

Example 3:

Input: the same tree, possible_anc_or_desc_0 = the node 5,
       possible_anc_or_desc_1 = the node 14, middle = the node 9
Output: False
Explanation: 5 and 14 are both descendants of 9.

Constraints:

    3 <= number of nodes <= 10^5
    The three nodes are distinct nodes of the same tree.

    REQUIRED: O(d) time when the answer is True, where d is the depth of
    the descendant minus the depth of the ancestor. O(h) time otherwise,
    for a tree of height h. O(1) extra space. NO parent pointers. NO
    recursion.
"""


class Solution:
    def pair_includes_ancestor_and_descendant_of_m(self, possible_anc_or_desc_0: TreeNode, possible_anc_or_desc_1: TreeNode, middle: TreeNode) -> bool:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.pair_includes_ancestor_and_descendant_of_m(find_node(t, 20), find_node(t, 11), find_node(t, 9)))  # True


def ordered(root: TreeNode, a: int, b: int, m: int) -> bool:
    return sol.pair_includes_ancestor_and_descendant_of_m(find_node(root, a), find_node(root, b), find_node(root, m))


# assert ordered(t, 20, 11, 9) is True
# assert ordered(t, 14, 20, 12) is True
# assert ordered(t, 5, 14, 9) is False
# assert ordered(t, 11, 20, 9) is True
# assert ordered(t, 20, 14, 12) is True
# assert ordered(t, 20, 25, 9) is False
# assert ordered(t, 25, 5, 20) is False
# assert ordered(t, 9, 14, 11) is False
# assert ordered(t, 9, 11, 12) is True
# assert ordered(t, 20, 9, 12) is False
# assert ordered(t, 11, 14, 12) is False
# assert ordered(t, 5, 11, 25) is False
# t = build_tree([2, 1, 3])
# assert ordered(t, 1, 3, 2) is False
# chain = build_tree([0] + [v for k in range(1, 499) for v in (None, k)])
# assert ordered(chain, 0, 498, 250) is True
# assert ordered(chain, 498, 0, 250) is True
# assert ordered(chain, 0, 250, 498) is False
# assert ordered(chain, 249, 251, 250) is True
