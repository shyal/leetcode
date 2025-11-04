"""
URL: https://leetcode.com/problems/binary-tree-level-order-traversal/description/

102. Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).


Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:

Input: root = [1]
Output: [[1]]

Example 3:

Input: root = []
Output: []


Constraints:

    The number of nodes in the tree is in the range [0, 2000].
    -1000 <= Node.val <= 1000

"""


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        def dfs(node, depth=0):
            if not node:
                return
            levels[depth].append(node.val)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        levels = defaultdict(list)

        dfs(root)
        return [x[1] for x in sorted(levels.items(), key=lambda x: x[0])]


sol = Solution()

tree = build_tree([3, 9, 20, None, None, 15, 7])
draw_tree(tree)
# print(sol.levelOrder(tree))  # [[3],[9,20],[15,7]]

assert sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [
    [3],
    [9, 20],
    [15, 7],
]
assert sol.levelOrder(build_tree([1])) == [[1]]
assert sol.levelOrder(build_tree([])) == []
assert sol.levelOrder(build_tree([1, 2])) == [[1], [2]]
assert sol.levelOrder(build_tree([1, None, 2])) == [[1], [2]]
assert sol.levelOrder(build_tree([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]
assert sol.levelOrder(build_tree([-5, 4, -3, None, None, 2, 1])) == [
    [-5],
    [4, -3],
    [2, 1],
]
assert sol.levelOrder(build_tree([1, 2, None, 3, None])) == [[1], [2], [3]]
assert sol.levelOrder(build_tree([1, None, 2, None, 3])) == [[1], [2], [3]]
assert sol.levelOrder(build_tree([0, 0, 0, 0, 0, 0, 0])) == [[0], [0, 0], [0, 0, 0, 0]]
