"""
Given the root node of a binary tree, return True when the tree is
balanced and False otherwise. A tree is balanced when, at every node,
the heights of the left subtree and the right subtree differ by at most
one. An empty tree is balanced.

Example 1:

Input: node = the root of

          a
         / \\
        b   c
       /     \\
      d       e
     /         \\
    f           g

Output: False
Explanation: the tree is symmetric, but at node b the left subtree has
height 2 and the right subtree has height 0.

Example 2:

Input: node = the root of

          a
         / \\
        b   c
       / \\   \\
      d   e   f

Output: True

Example 3:

Input: node = the root of

      a
     / \\
    b   c
         \\
          d
           \\
            e

Output: False
Explanation: at node c the right subtree has height 2 and the left has
height 0.

Constraints:

    0 <= number of nodes <= 10^4
    Node values are single lowercase letters.

    REQUIRED: O(n) time, where n is the number of nodes. NO recomputing
    the height of a subtree.
"""


class Solution:
    def is_balanced(self, node: TreeNode | None) -> bool:
        pass


sol = Solution()

root = build_tree(["a", "b", "c", "d", None, None, "e", "f", None, None, "g"])
draw_tree(root)
print(sol.is_balanced(root))  # False

# assert sol.is_balanced(build_tree(["a", "b", "c", "d", None, None, "e", "f", None, None, "g"])) is False
# assert sol.is_balanced(build_tree(["a", "b", "c", "d", "e", None, "f"])) is True
# assert sol.is_balanced(build_tree(["a", "b", "c", None, None, None, "d", None, "e"])) is False
# assert sol.is_balanced(build_tree(["a", "b", "c", None, None, None, "d"])) is True
# assert sol.is_balanced(build_tree(["a"])) is True
# assert sol.is_balanced(None) is True
# assert sol.is_balanced(build_tree(["a", "b"])) is True
# assert sol.is_balanced(build_tree(["a", "b", None, "c"])) is False
# assert sol.is_balanced(build_tree(["a", "b", "c", "d", "e", "f", "g"])) is True
# assert sol.is_balanced(build_tree(["a", "b", "c", "d", "e", "f", "g", "h", None, None, None, None, None, None, None, "i"])) is False
# chain = reduce(lambda t, k: TreeNode("b", None, t), range(499), TreeNode("a"))
# assert sol.is_balanced(chain) is False
# fork = TreeNode("a", chain, TreeNode("c"))
# assert sol.is_balanced(fork) is False
# full = build_tree(["a"] * (2 ** 13 - 1))
# assert sol.is_balanced(full) is True
