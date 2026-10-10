"""
URL: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

987. Vertical Order Traversal of a Binary Tree

Given the root of a binary tree, calculate the vertical order traversal of the binary tree.

For each node at position (row, col), its left and right children will be at positions (row + 1, col - 1) and (row + 1, col + 1) respectively. The root of the tree is at (0, 0).

The vertical order traversal of a binary tree is a list of top-to-bottom orderings for each column index starting from the leftmost column and ending on the rightmost column. There may be multiple nodes in the same row and same column. In such a case, sort these nodes by their values.

Return the vertical order traversal of the binary tree.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]
Explanation:
Column -1: Only node 9 is in this column.
Column 0: Nodes 3 and 15 are in this column in that order from top to bottom.
Column 1: Only node 20 is in this column.
Column 2: Only node 7 is in this column.

Example 2:

Input: root = [1,2,3,4,5,6,7]
Output: [[4],[2],[1,5,6],[3],[7]]
Explanation:
Column -2: Only node 4 is in this column.
Column -1: Only node 2 is in this column.
Column 0: Nodes 1, 5, and 6 are in this column.
          1 is at the top, so it comes first.
          5 and 6 are at the same position (2, 0), so we order them by their value, 5 before 6.
Column 1: Only node 3 is in this column.
Column 2: Only node 7 is in this column.

Example 3:

Input: root = [1,2,3,4,6,5,7]
Output: [[4],[2],[1,5,6],[3],[7]]
Explanation:
This case is the exact same as example 2, but with nodes 5 and 6 swapped.
Note that the solution remains the same since 5 and 6 are in the same location and should be ordered by their values.

Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    0 <= Node.val <= 1000
---
Hinted with: out[c].extend(sorted(res[r][c])) and return [out[c] for c in min_col..max_col]

LEETCODE: Accepted (1 ms, 19.7 MB)
"""


# mu 0.7
# def verticalTraversal(root: TreeNode?) -> [[int]]
#   def bfs()
#     q = deque([(root, 0, 0)])
#     while q
#       node, row, col = q.popleft()
#       if node
#         res[row][col] <- node.val
#         q <- (node.right, row + 1, col + 1)
#         q <- (node.left, row + 1, col - 1)
#
#   res = {:() -> {:list}}
#   bfs()
#
#   min_row, max_row = min(res), max(res)
#   min_col, max_col = inf, 0
#   for r in res
#     for c in res[r]
#       min_col = min(min_col, c)
#       max_col = max(max_col, c)
#       print(r, c, res[r][c])
#   out = {:list}
#   for c in min_col..max_col
#     for r in min_row..max_row
#       if res[r][c]
#         out[c].extend(sorted(res[r][c]))
#
#   return [out[c] for c in min_col..max_col]
#

from collections import defaultdict
from math import inf
from typing import Optional


class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> list[list[int]]:
        def bfs():
            q = deque([(root, 0, 0)])
            while q:
                node, row, col = q.popleft()
                if node:
                    res[row][col].append(node.val)
                    q.append((node.right, row + 1, col + 1))
                    q.append((node.left, row + 1, col - 1))
        res = defaultdict(lambda: defaultdict(list))
        bfs()
        min_row, max_row = min(res), max(res)
        min_col, max_col = inf, 0
        for r in res:
            for c in res[r]:
                min_col = min(min_col, c)
                max_col = max(max_col, c)
                print(r, c, res[r][c])
        out = defaultdict(list)
        for c in range(min_col, max_col + 1):
            for r in range(min_row, max_row + 1):
                if res[r][c]:
                    out[c].extend(sorted(res[r][c]))
        return [out[c] for c in range(min_col, max_col + 1)]


sol = Solution()
root = build_tree([3, 9, 20, None, None, 15, 7])
print(root)
print(sol.verticalTraversal(root))
