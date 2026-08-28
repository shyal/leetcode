"""
DRILL: Count Univalue Subtrees
TRAINS: tree-global-across-subtrees

Given the root of a binary tree, return the number of univalue subtrees.
A subtree is a node together with all of its descendants. A subtree is
univalue when every node in it holds the same value.

Example 1:

Input: root = [5, 1, 5, 5, 5, None, 5]
Output: 4
Explanation: the three leaf 5s, plus the right child of the root: it
holds 5 and its only descendant holds 5.

Example 2:

Input: root = [7]
Output: 1
Explanation: a leaf is a univalue subtree.

Example 3:

Input: root = [1, 1, 2]
Output: 2
Explanation: both leaves qualify. The whole tree holds two values, so
it does not.

Constraints:

    1 <= number of nodes <= 1000
    -100 <= Node.val <= 100

    REQUIRED: one pass, O(n). The count must accumulate outside the
    recursion's returns. Threading the count through the return, or
    re-walking a subtree to test it, is the failure mode this drill
    exists to kill. NO tuple returns bundling the count, NO second
    traversal.
"""


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        def DP(n):
            if not n:
                return None

            left = DP(n.left) or n.val
            right = DP(n.right) or n.val

            if left == right == n.val:
                self.count += 1
                return n.val

            return -1

        self.count = 0

        DP(root)

        return self.count


sol = Solution()

tree = build_tree([5, 1, 5, 5, 5, None, 5])
draw_tree(tree)

print(sol.countUnivalSubtrees(tree))  # 4

assert sol.countUnivalSubtrees(build_tree([5, 1, 5, 5, 5, None, 5])) == 4
assert sol.countUnivalSubtrees(build_tree([7])) == 1
assert sol.countUnivalSubtrees(build_tree([1, 1, 2])) == 2
assert sol.countUnivalSubtrees(build_tree([2, 2, 2])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, None, 5])) == 6
assert sol.countUnivalSubtrees(build_tree([1, 1, 1, 1, 1, 1, 1])) == 7
assert sol.countUnivalSubtrees(build_tree([1, None, 1, None, 1])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, 5, 9])) == 5
assert sol.countUnivalSubtrees(build_tree([1, 2, 3])) == 2
