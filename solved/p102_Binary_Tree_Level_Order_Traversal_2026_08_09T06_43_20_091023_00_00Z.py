"""
URL: https://leetcode.com/problems/binary-tree-level-order-traversal/description/?envType=problem-list-v2&envId=vn57k9wr

102. Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).


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
        queue = deque([root])
        vals = []
        while root and queue:
            lvals = []
            new_queue = deque([])
            for node in queue:
                lvals.append(node.val)
                if node.left:
                    new_queue.append(node.left)
                if node.right:
                    new_queue.append(node.right)
            vals.append(lvals)
            queue = new_queue
        return vals
                

sol = Solution()

# draw_tree(build_tree([3, 9, 20, None, None, 15, 7]))
# print(sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])))  # [[3], [9, 20], [15, 7]]

assert sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
assert sol.levelOrder(build_tree([1])) == [[1]]
assert sol.levelOrder(build_tree([])) == []
assert sol.levelOrder(None) == []
assert sol.levelOrder(build_tree([0])) == [[0]]
assert sol.levelOrder(build_tree([-1000])) == [[-1000]]
assert sol.levelOrder(build_tree([1000])) == [[1000]]
assert sol.levelOrder(build_tree([1, 2, None, 3, None])) == [[1], [2], [3]]
assert sol.levelOrder(build_tree([1, None, 2, None, 3])) == [[1], [2], [3]]
assert sol.levelOrder(build_tree([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]
assert sol.levelOrder(build_tree([1, 2, 3, None, 4, None, 5])) == [[1], [2, 3], [4, 5]]
assert sol.levelOrder(build_tree([1, 2, 3, 4, None, None, 5])) == [[1], [2, 3], [4, 5]]
assert sol.levelOrder(build_tree([5, 5, 5])) == [[5], [5, 5]]
assert sol.levelOrder(build_tree([1, -2, 3, 4, None, None, -5])) == [[1], [-2, 3], [4, -5]]
assert sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7, 1, 2])) == [[3], [9, 20], [15, 7], [1, 2]]
assert sol.levelOrder(build_tree([1, 2, 3, None, None, 4, None, None, 5])) == [[1], [2, 3], [4], [5]]