"""
URL: https://leetcode.com/problems/flatten-binary-tree-to-linked-list/description/

114. Flatten Binary Tree to Linked List

Given the root of a binary tree, flatten the tree into a "linked list":

    The "linked list" should use the same TreeNode class where the right child pointer points to the next node in the list and the left child pointer is always null.
    The "linked list" should be in the same order as a pre-order traversal of the binary tree.


Example 1:

Input: root = [1,2,5,3,4,null,6]
Output: [1,null,2,null,3,null,4,null,5,null,6]

Example 2:

Input: root = []
Output: []

Example 3:

Input: root = [0]
Output: [0]


Constraints:

    The number of nodes in the tree is in the range [0, 2000].
    -100 <= Node.val <= 100


Follow up: Can you flatten the tree in-place (with O(1) extra space)?

---

Hmm i didn't understand the question initially, i didn't realize the tree
has to be mutated, rather than return a new linked list.

Hmm not super happy with this solve. It feels a little 'brute force'.

Tip: read the question properly next time.

"""


class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        def pre_order(node):
            if not node:
                return
            res.append(node.val)
            pre_order(node.left)
            pre_order(node.right)

        if not root:
            return

        res = []
        pre_order(root)
        new = TreeNode(-1, None, None)
        it = new
        for r in res:
            it.right = TreeNode(r)
            it = it.right
        root.right = new.right.right if new.right else None
        root.left = None


sol = Solution()
tree = build_tree([1, 2, 5, 3, 4, None, 6])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 2, 3, 4, 5, 6]

sol = Solution()
tree = build_tree([])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == []

sol = Solution()
tree = build_tree([0])
draw_tree(tree)
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [0]

sol = Solution()
tree = build_tree([1, 2, 5, 3, 4, None, 6])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 2, 3, 4, 5, 6]

sol = Solution()
tree = build_tree([])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == []

sol = Solution()
tree = build_tree([0])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [0]

sol = Solution()
tree = build_tree([2, 1])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [2, 1]

sol = Solution()
tree = build_tree([2, None, 1])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [2, 1]

sol = Solution()
tree = build_tree([1, 2, None, 3])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 2, 3]

sol = Solution()
tree = build_tree([1, None, 2, None, 3])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 2, 3]

sol = Solution()
tree = build_tree([1, 2, 3, 4])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 2, 4, 3]

sol = Solution()
tree = build_tree([-5, -10, -3])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [-5, -10, -3]

sol = Solution()
tree = build_tree([1, 1, 1])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [1, 1, 1]

sol = Solution()
tree = build_tree([-100])
sol.flatten(tree)
actual = []
curr = tree
while curr:
    actual.append(curr.val)
    assert curr.left is None
    curr = curr.right
assert actual == [-100]
