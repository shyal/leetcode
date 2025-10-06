"""
URL: https://leetcode.com/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/description/

1379. Find a Corresponding Node of a Binary Tree in a Clone of That Tree

Given two binary trees original and cloned and given a reference to a node target in the original tree.

The cloned tree is a copy of the original tree.

Return a reference to the same node in the cloned tree.

Note that you are not allowed to alter any of the two trees or the target node and the answer must be a reference to a node in the cloned tree.


Example 1:

Input: tree = [7,4,3,null,null,6,19], target = 3
Output: 3

Example 2:

Input: tree = [7], target =  7
Output: 7

Example 3:

Input: tree = [8,null,6,null,5,null,4,null,3,null,2,null,1], target = 4
Output: 4


Constraints:

    The number of nodes in the tree is in the range [1, 104].
    The values of the nodes of the tree are unique.
    target node is a node from the original tree and is not null.


Follow up: Could you solve this in O(n) time?
"""


class Solution:
    def getTargetCopy(
        self, original: TreeNode, cloned: TreeNode, target: TreeNode
    ) -> TreeNode:
        def dfs(node):
            if not node:
                return
            if node.val == target.val:
                return node
            return dfs(node.left) or dfs(node.right)

        return dfs(cloned)


sol = Solution()

original = build_tree([7, 4, 3, None, None, 6, 19])
cloned = build_tree([7, 4, 3, None, None, 6, 19])
target = find_node(original, 3)
# print(sol.getTargetCopy(original, cloned, target).val)  # 3

original = build_tree([7, 4, 3, None, None, 6, 19])
cloned = build_tree([7, 4, 3, None, None, 6, 19])
target = find_node(original, 3)
assert sol.getTargetCopy(original, cloned, target).val == 3

original = build_tree([7])
cloned = build_tree([7])
target = find_node(original, 7)
assert sol.getTargetCopy(original, cloned, target).val == 7

original = build_tree([8, None, 6, None, 5, None, 4, None, 3, None, 2, None, 1])
cloned = build_tree([8, None, 6, None, 5, None, 4, None, 3, None, 2, None, 1])
target = find_node(original, 4)
assert sol.getTargetCopy(original, cloned, target).val == 4

original = build_tree([7, 4, 3, None, None, 6, 19])
cloned = build_tree([7, 4, 3, None, None, 6, 19])
target = find_node(original, 4)
assert sol.getTargetCopy(original, cloned, target).val == 4

original = build_tree([7, 4, 3, None, None, 6, 19])
cloned = build_tree([7, 4, 3, None, None, 6, 19])
target = find_node(original, 19)
assert sol.getTargetCopy(original, cloned, target).val == 19

original = build_tree([1, 2, None, 3, None])
cloned = build_tree([1, 2, None, 3, None])
target = find_node(original, 3)
assert sol.getTargetCopy(original, cloned, target).val == 3

original = build_tree([1, None, 2, None, 3])
cloned = build_tree([1, None, 2, None, 3])
target = find_node(original, 3)
assert sol.getTargetCopy(original, cloned, target).val == 3

original = build_tree([7, 4, 3, None, None, 6, 19])
cloned = build_tree([7, 4, 3, None, None, 6, 19])
target = original
assert sol.getTargetCopy(original, cloned, target).val == 7
