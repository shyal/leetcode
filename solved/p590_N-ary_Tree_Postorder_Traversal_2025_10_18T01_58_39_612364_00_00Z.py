"""
URL: https://leetcode.com/problems/n-ary-tree-postorder-traversal/description/

590. N-ary Tree Postorder Traversal

Given the root of an n-ary tree, return the postorder traversal of its nodes' values.

Nary-Tree input serialization is represented in their level order traversal. Each group of children is separated by the null value (See examples).


Example 1:

Input: root = [1,null,3,2,4,null,5,6]
Output: [5,6,3,2,4,1]

Example 2:

Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [2,6,14,11,7,3,12,8,4,13,9,10,5,1]


Constraints:

    The number of nodes in the tree is in the range [0, 10^4].
    0 <= Node.val <= 10^4
    The height of the n-ary tree is less than or equal to 1000.


Follow up: Recursive solution is trivial, could you do it iteratively?
"""


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []


class Solution:
    def postorder(self, root: "Node") -> List[int]:
        def dfs(node):
            if not node:
                return
            for c in node.children:
                dfs(c)
            res.append(node.val)

        res = []
        dfs(root)
        return res


sol = Solution()

# Example 1
root1 = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
# print(sol.postorder(root1))  # [5, 6, 3, 2, 4, 1]

# Example 2
root2 = Node(
    1,
    [
        Node(2),
        Node(3, [Node(6), Node(7, [Node(11, [Node(14)])])]),
        Node(4, [Node(8, [Node(12)])]),
        Node(5, [Node(9, [Node(13)]), Node(10)]),
    ],
)

assert sol.postorder(root1) == [5, 6, 3, 2, 4, 1]
assert sol.postorder(root2) == [2, 6, 14, 11, 7, 3, 12, 8, 4, 13, 9, 10, 5, 1]

root_empty = None
assert sol.postorder(root_empty) == []

root_single = Node(1)
assert sol.postorder(root_single) == [1]

root_zero = Node(0)
assert sol.postorder(root_zero) == [0]

root_linear = Node(1, [Node(2, [Node(3, [Node(4)])])])
assert sol.postorder(root_linear) == [4, 3, 2, 1]

root_many_children = Node(1, [Node(i) for i in range(2, 7)])
assert sol.postorder(root_many_children) == [2, 3, 4, 5, 6, 1]

root_with_empty_children = Node(1, [Node(2, []), Node(3)])
assert sol.postorder(root_with_empty_children) == [2, 3, 1]
