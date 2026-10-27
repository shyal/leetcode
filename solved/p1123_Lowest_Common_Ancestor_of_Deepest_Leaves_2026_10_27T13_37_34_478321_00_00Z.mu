# URL: https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1123. Lowest Common Ancestor of Deepest Leaves
#
# Given the root of a binary tree, return the lowest common ancestor of its deepest leaves.
#
# Recall that:
# - The node of a binary tree is a leaf if and only if it has no children.
# - The depth of the root of the tree is 0. If the depth of a node is d, the depth of each of its children is d + 1.
# - The lowest common ancestor of a set S of nodes, is the node A with the largest depth such that every node in S is in the subtree with root A.
#
# Example 1:
#
# Input: root = [3,5,1,6,2,0,8,null,null,7,4]
# Output: [2,7,4]
# Explanation: We return the node with value 2, colored in yellow in the diagram.
# The nodes coloured in blue are the deepest leaf-nodes of the tree.
# Note that nodes 6, 0, and 8 are also leaf nodes, but the depth of them is 2, but the depth of nodes 7 and 4 is 3.
#
# Example 2:
#
# Input: root = [1]
# Output: [1]
# Explanation: The root is the deepest node in the tree, and it's the lca of itself.
#
# Example 3:
#
# Input: root = [0,1,3,null,2]
# Output: [2]
# Explanation: The deepest leaf node in the tree is 2, the lca of one node is itself.
#
# Constraints:
#
#     The number of nodes in the tree will be in the range [1, 1000].
#     0 <= Node.val <= 1000
#     The values of the nodes in the tree are unique.
#
# Note: This question is the same as 865: https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/
#
# ---
# LEETCODE: Accepted (3 ms, 19.8 MB)

# mu 0.13

class Solution
  def lcaDeepestLeaves(root: TreeNode?) -> TreeNode?
    self.levels = {:list}
    {
      (n, d) -> 
        if n is none
          return
        self.levels[d] <- n.val
        mu(n.left, d + 1)
        mu(n.right, d + 1)
    }(root, 0)
    deepest = set(self.levels[max(self.levels)])
    self.lca = None
    {
      (n) -> 
        if n is none
          return
        if len deepest == 1 and n.val in deepest
          self.lca = n
          return True
        left = mu(n.left)
        right = mu(n.right)
        if left and right or ((left and n in deepest) or (right and n in deepest))
          self.lca = n
        left or right or ((left and n in deepest) or (right and n in deepest)) or n.val in deepest
        
    }(root)
    self.lca

sol = Solution()

root = build_tree([3, 5, 1, 6, 2, 0, 8, none, none, 7, 4])
print(root)

print(sol.lcaDeepestLeaves(root).val)  # 2

assert sol.lcaDeepestLeaves(build_tree([3, 5, 1, 6, 2, 0, 8, none, none, 7, 4])).val == 2
assert sol.lcaDeepestLeaves(build_tree([1])).val == 1
assert sol.lcaDeepestLeaves(build_tree([0, 1, 3, none, 2])).val == 2
assert sol.lcaDeepestLeaves(build_tree([1, 2, 3, 4, none, none, 5, none, 6, none, none, none, 7])).val == 7
assert sol.lcaDeepestLeaves(build_tree([1, 2, 3, 4, 5, 6, 7, 8, none, none, none, none, none, none, 9])).val == 1
assert sol.lcaDeepestLeaves(build_tree([1])).val == 1
assert sol.lcaDeepestLeaves(build_tree([1, 2, none, 3, none, 4, none, 5])).val == 5
assert sol.lcaDeepestLeaves(build_tree([1, none, 2, none, 3, none, 4, none, 5])).val == 5
assert sol.lcaDeepestLeaves(build_tree([1, 2, 3, 4, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1])).val == 1
tree = build_tree([1000, 999, 998, 997, 996, 995, 994, 993, 992, 991, 990])
assert sol.lcaDeepestLeaves(tree).val == 999
assert sol.lcaDeepestLeaves(build_tree([0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10])).val == -1
assert sol.lcaDeepestLeaves(build_tree([1, 2, 3, 4, none, none, 5, none, none, none, 6])).val == 6
assert sol.lcaDeepestLeaves(build_tree([1, none, 2, none, 3, none, 4, none, 5, none, 6])).val == 6
assert sol.lcaDeepestLeaves(build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])).val == 1
