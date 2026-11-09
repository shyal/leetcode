"""
EPI 15.9 Generate binary trees

Given num_nodes, return the roots of every binary tree with exactly
num_nodes nodes, each tree once. Two trees are the same when they have
the same shape; node values do not count. Give every node the value 0.
Return the roots in any order. The tree with no nodes is None.

Example 1:

Input: num_nodes = 3
Output: the roots of the five trees

        0          0          0          0          0
       /          /          / \\          \\          \\
      0          0          0   0          0          0
     /            \\                       /            \\
    0              0                     0              0

Example 2:

Input: num_nodes = 1
Output: [TreeNode(0)]

Example 3:

Input: num_nodes = 0
Output: [None]
Explanation: the empty tree, None, is the only tree with no nodes.

Constraints:

    0 <= num_nodes <= 10

    REQUIRED: O(num_nodes * C) time, where C is the number of trees
    returned. NO generation of shapes followed by a test for
    duplicates.
"""


class Solution:
    def generate_all_binary_trees(self, num_nodes: int) -> list[TreeNode | None]:
        pass


sol = Solution()


def form(t):
    """The shape of a tree as a string: "." for None, "(LR)" for a node."""
    return "." if t is None else "(" + form(t.left) + form(t.right) + ")"


for root in sol.generate_all_binary_trees(3) or []:
    draw_tree(root)

# assert [form(t) for t in sol.generate_all_binary_trees(0)] == ["."]
# assert [form(t) for t in sol.generate_all_binary_trees(1)] == ["(..)"]
# assert sorted(form(t) for t in sol.generate_all_binary_trees(2)) == ["((..).)", "(.(..))"]
# assert sorted(form(t) for t in sol.generate_all_binary_trees(3)) == ["(((..).).)", "((.(..)).)", "((..)(..))", "(.((..).))", "(.(.(..)))"]
# trees = [form(t) for t in sol.generate_all_binary_trees(4)]
# assert len(trees) == 14 and len(set(trees)) == 14
# assert all(f.count("(") == 4 for f in trees)
# trees = [form(t) for t in sol.generate_all_binary_trees(5)]
# assert len(trees) == 42 and len(set(trees)) == 42
# assert all(f.count("(") == 5 for f in trees)
# trees = [form(t) for t in sol.generate_all_binary_trees(7)]
# assert len(trees) == 429 and len(set(trees)) == 429
# trees = [form(t) for t in sol.generate_all_binary_trees(10)]
# assert len(trees) == 16796 and len(set(trees)) == 16796
# assert all(f.count("(") == 10 for f in trees)
# assert "(" * 10 + "..)" + ".)" * 9 in trees
