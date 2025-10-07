"""
URL: https://leetcode.com/problems/evaluate-boolean-binary-tree/description/

2331. Evaluate Boolean Binary Tree

You are given the root of a full binary tree with the following properties:

    Leaf nodes have either the value 0 or 1, where 0 represents False and 1 represents True.
    Non-leaf nodes have either the value 2 or 3, where 2 represents the boolean OR and 3 represents the boolean AND.

The evaluation of a node is as follows:

    If the node is a leaf node, the evaluation is the value of the node, i.e. True or False.
    Otherwise, evaluate the node's two children and apply the boolean operation of its value with the children's evaluations.

Return the boolean result of evaluating the root node.

A full binary tree is a binary tree where a node has either 0 or 2 children.


Example 1:

Input: root = [2,1,3,null,null,0,1]
Output: true
Explanation: The above diagram illustrates the evaluation process.
The AND node evaluates to false AND true = false.
The OR node evaluates to true OR false = true.
The root node evaluates to true, so we return true.

Example 2:

Input: root = [0]
Output: false
Explanation: The root node is a leaf node and it evaluates to false, so we return false.


Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    0 <= Node.val <= 3
    Every node has either 0 or 2 children.
    Leaf nodes have a value of 0 or 1.
    Non-leaf nodes have a value of 2 or 3.

"""

from operator import or_, and_


class Solution:
    def evaluateTree(self, root: Optional[TreeNode]) -> bool:
        def dfs(node):
            is_leaf = node.left is None and node.right is None
            if is_leaf:
                return bool(node.val)
            left = dfs(node.left)
            right = dfs(node.right)
            return ops[node.val](left, right)

        ops = {2: or_, 3: and_}

        return dfs(root) if root else False


sol = Solution()

tree = build_tree([2, 1, 3, None, None, 0, 1])
# draw_tree(tree)
# print(sol.evaluateTree(tree))  # True

assert sol.evaluateTree(build_tree([2, 1, 3, None, None, 0, 1])) == True
assert sol.evaluateTree(build_tree([0])) == False
assert sol.evaluateTree(build_tree([1])) == True
assert sol.evaluateTree(build_tree([2, 0, 0])) == False
assert sol.evaluateTree(build_tree([2, 0, 1])) == True
assert sol.evaluateTree(build_tree([2, 1, 0])) == True
assert sol.evaluateTree(build_tree([2, 1, 1])) == True
assert sol.evaluateTree(build_tree([3, 0, 0])) == False
assert sol.evaluateTree(build_tree([3, 0, 1])) == False
assert sol.evaluateTree(build_tree([3, 1, 0])) == False
assert sol.evaluateTree(build_tree([3, 1, 1])) == True
assert sol.evaluateTree(build_tree([2, 0, 2, None, None, 0, 0])) == False
assert sol.evaluateTree(build_tree([3, 2, 2, 0, 1, 0, 0])) == False
assert sol.evaluateTree(build_tree([3, 2, 2, 0, 1, 1, 0])) == True
assert sol.evaluateTree(None) == False
