"""
URL: https://leetcode.com/problems/binary-tree-level-order-traversal/description/?envType=problem-list-v2&envId=vn57k9wr

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
        q = deque([[root, 0]])
        levels = defaultdict(list)
        while q:
            node, level = q.popleft()
            if node:
                levels[level].append(node.val)

                if node.left:
                    q.append([node.left, level + 1])
                if node.right:
                    q.append([node.right, level + 1])
        return [levels[x] for x in sorted(levels)]


sol = Solution()

print(sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])))  # [[3],[9,20],[15,7]]

assert sol.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [
    [3],
    [9, 20],
    [15, 7],
]
assert sol.levelOrder(build_tree([1])) == [[1]]
assert sol.levelOrder(build_tree([])) == []

assert sol.levelOrder(build_tree([1, 1, 1, 1, 1, 1, 1])) == [[1], [1, 1], [1, 1, 1, 1]]
assert sol.levelOrder(build_tree([-1, -2, -3, -4, -5, -6, -7])) == [
    [-1],
    [-2, -3],
    [-4, -5, -6, -7],
]
assert sol.levelOrder(build_tree([0] * 10)) == [[0], [0, 0], [0, 0, 0, 0], [0, 0, 0]]
assert sol.levelOrder(build_tree([1000, -1000, 500, -500, None, None, 0])) == [
    [1000],
    [-1000, 500],
    [-500, 0],
]
assert sol.levelOrder(build_tree([1, None, 2, None, 3, None, 4, None, 5])) == [
    [1],
    [2],
    [3],
    [4],
    [5],
]
assert sol.levelOrder(build_tree([5, 4, 6, None, None, None, 7])) == [[5], [4, 6], [7]]
assert sol.levelOrder(build_tree([None])) == []
assert sol.levelOrder(build_tree([1, 2, 3, 4, None, None, 5, None, None, 6])) == [
    [1],
    [2, 3],
    [4, 5],
    [6],
]
assert sol.levelOrder(build_tree([i if i % 2 == 0 else None for i in range(15)])) == [
    [0],
    [2],
    [4],
    [6],
    [8],
    [10],
    [12],
    [14],
]
assert sol.levelOrder(build_tree([1, -1, 1, -1, 1, -1, 1])) == [
    [1],
    [-1, 1],
    [-1, 1, -1, 1],
]
