"""
URL: https://leetcode.com/problems/binary-tree-paths/description/

257. Binary Tree Paths

Given the root of a binary tree, return all root-to-leaf paths in any order.

A leaf is a node with no children.


Example 1:

Input: root = [1,2,3,null,5]
Output: ["1->2->5","1->3"]

Example 2:

Input: root = [1]
Output: ["1"]


Constraints:

    The number of nodes in the tree is in the range [1, 100].
    -100 <= Node.val <= 100
"""


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        def dfs(node, path=[]):
            if not node:
                return
            copy = path + [str(node.val)]
            dfs(node.left, copy)
            dfs(node.right, copy)
            if node.left is None and node.right is None:
                paths.append("->".join(copy))

        paths = []
        dfs(root)
        return paths


sol = Solution()
tree = build_tree([1, 2, 3, None, 5])
assert sol.binaryTreePaths(tree) == ["1->2->5", "1->3"]
tree = build_tree([1])
assert sol.binaryTreePaths(tree) == ["1"]
tree = build_tree([1, 2])
assert sol.binaryTreePaths(tree) == ["1->2"]
tree = build_tree([1, None, 2])
assert sol.binaryTreePaths(tree) == ["1->2"]
tree = build_tree([1, 2, 3, 4])
assert sol.binaryTreePaths(tree) == ["1->2->4", "1->3"]
tree = build_tree([1, 2, 3, 4, 5])
assert sol.binaryTreePaths(tree) == ["1->2->4", "1->2->5", "1->3"]
tree = build_tree([1, -2, 3, None, -5])
assert sol.binaryTreePaths(tree) == ["1->-2->-5", "1->3"]
tree = build_tree([1, 2, None, 3])
assert sol.binaryTreePaths(tree) == ["1->2->3"]
tree = build_tree([1, 2, 3])
assert sol.binaryTreePaths(tree) == ["1->2", "1->3"]
tree = build_tree([-100])
assert sol.binaryTreePaths(tree) == ["-100"]
tree = build_tree([1, 2, None, 3, None, 4, None])
assert sol.binaryTreePaths(tree) == ["1->2->3->4"]
tree = build_tree([1, None, 2, None, 3])
assert sol.binaryTreePaths(tree) == ["1->2->3"]
