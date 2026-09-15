"""
DRILL: Count Univalue Subtrees

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
        def helper(n):
            if not n:
                return True, None

            unis = []
            vals = [n.val]
            if n.left:
                uni, val = helper(n.left)
                unis.append(uni)
                vals.append(val)
            if n.right:
                uni, val = helper(n.right)
                unis.append(uni)
                vals.append(val)

            vals_all_same = len(set(vals)) == 1
            unis_all_same = all(unis) or len(unis) == 0
            if vals_all_same and unis_all_same:
                self.count += 1

            return unis_all_same and vals_all_same, vals[0]

        self.count = 0
        helper(root)
        return self.count


sol = Solution()

tree = build_tree([5, 5, 5, 5, 5, 5, 9])
print(sol.countUnivalSubtrees(tree))  # 5
print(tree)


# tree = build_tree([5, 1, 5, 5, 5, None, 5])
# print(tree)

# print(sol.countUnivalSubtrees(tree))  # 4

assert sol.countUnivalSubtrees(build_tree([5, 1, 5, 5, 5, None, 5])) == 4
assert sol.countUnivalSubtrees(build_tree([7])) == 1
assert sol.countUnivalSubtrees(build_tree([1, 1, 2])) == 2
assert sol.countUnivalSubtrees(build_tree([2, 2, 2])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, None, 5])) == 6
assert sol.countUnivalSubtrees(build_tree([1, 1, 1, 1, 1, 1, 1])) == 7
assert sol.countUnivalSubtrees(build_tree([1, None, 1, None, 1])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, 5, 9])) == 5
assert sol.countUnivalSubtrees(build_tree([1, 2, 3])) == 2
