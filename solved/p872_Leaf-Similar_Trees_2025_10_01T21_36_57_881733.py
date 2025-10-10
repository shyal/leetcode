"""
https://leetcode.com/problems/leaf-similar-trees/description/

872. Leaf-Similar Trees
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.

For example, in the given tree above, the leaf value sequence is (6, 7, 4, 9, 8).

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

Example 1:

Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true
Example 2:

Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false

Constraints:

The number of nodes in each tree will be in the range [1, 200].
Both of the given trees will have values in the range [0, 200].
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:

        def dfs(node, leaves):
            if not node:
                return
            is_leaf = node.left == node.right == None
            if is_leaf:
                leaves.append(node.val)
                return
            dfs(node.left, leaves)
            dfs(node.right, leaves)

        leaves1 = []
        leaves2 = []
        dfs(root1, leaves1)
        dfs(root2, leaves2)
        return leaves1 == leaves2


sol = Solution()

root1 = TreeNode(
    3,
    TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))),
    TreeNode(1, TreeNode(9), TreeNode(8)),
)
root2 = TreeNode(
    3,
    TreeNode(5, TreeNode(6), TreeNode(7)),
    TreeNode(1, TreeNode(4), TreeNode(2, TreeNode(9), TreeNode(8))),
)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2), TreeNode(3))
root2 = TreeNode(1, TreeNode(3), TreeNode(2))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1)
root2 = TreeNode(1)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1)
root2 = TreeNode(2)
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2))
root2 = TreeNode(1, None, TreeNode(2))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2))
root2 = TreeNode(1, None, TreeNode(3))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
root2 = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
root2 = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4)))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(0, TreeNode(1), TreeNode(1))
root2 = TreeNode(0, TreeNode(1), TreeNode(1))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(0, TreeNode(1, TreeNode(3)))
root2 = TreeNode(3)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(0, TreeNode(0))
root2 = TreeNode(0, None, TreeNode(0))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(200, TreeNode(0, TreeNode(0), TreeNode(0)), TreeNode(0))
root2 = TreeNode(100, TreeNode(0), TreeNode(0, TreeNode(0), TreeNode(0)))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, None, TreeNode(2, TreeNode(3)))
root2 = TreeNode(1, TreeNode(2, None, TreeNode(3)))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2, TreeNode(3)))
root2 = TreeNode(3, TreeNode(2), TreeNode(1))
assert sol.leafSimilar(root1, root2) == False


