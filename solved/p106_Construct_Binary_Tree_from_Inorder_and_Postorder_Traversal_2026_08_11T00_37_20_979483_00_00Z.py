"""
URL: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/?envType=problem-list-v2&envId=vn57k9wr

106. Construct Binary Tree from Inorder and Postorder Traversal

Given two integer arrays inorder and postorder where inorder is the inorder
traversal of a binary tree and postorder is the postorder traversal of the same
tree, construct and return the binary tree.


Example 1:

Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: inorder = [-1], postorder = [-1]
Output: [-1]


Constraints:

    1 <= inorder.length <= 3000
    postorder.length == inorder.length
    -3000 <= inorder[i], postorder[i] <= 3000
    inorder and postorder consist of unique values.
    Each value of postorder also appears in inorder.
    inorder is guaranteed to be the inorder traversal of the tree.
    postorder is guaranteed to be the postorder traversal of the tree.
"""


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not inorder:
            return None
        po_root_ind = len(postorder) -1
        in_root_ind = inorder.index(postorder[po_root_ind])
        in_left_subtree = inorder[:in_root_ind]
        in_right_subtree = inorder[in_root_ind + 1:]
        po_right_subtree = postorder[-len(in_right_subtree) -1:-1]
        po_left_subtree = postorder[:-len(po_right_subtree) -1]
        return TreeNode(inorder[in_root_ind], self.buildTree(in_left_subtree, po_left_subtree), self.buildTree(in_right_subtree, po_right_subtree))



sol = Solution()

# draw_tree(sol.buildTree([8, 9, 3, 15, 20, 7], [8, 9, 15, 7, 20, 3]))

assert get_level_order(sol.buildTree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])) == [
    3,
    9,
    20,
    None,
    None,
    15,
    7,
]
assert get_level_order(sol.buildTree([-1], [-1])) == [-1]

root = sol.buildTree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
assert root.val == 3
assert root.left.val == 9
assert root.right.val == 20
assert root.left.left is None
assert root.left.right is None
assert root.right.left.val == 15
assert root.right.right.val == 7
assert root.right.left.left is None
assert root.right.right.right is None

assert get_level_order(sol.buildTree([0], [0])) == [0]
assert get_level_order(sol.buildTree([3000], [3000])) == [3000]
assert get_level_order(sol.buildTree([-3000], [-3000])) == [-3000]

assert get_level_order(sol.buildTree([1, 2], [1, 2])) == [2, 1]
assert get_level_order(sol.buildTree([1, 2], [2, 1])) == [1, None, 2]

assert get_level_order(sol.buildTree([1, 2, 3], [1, 2, 3])) == [3, 2, None, 1]
assert get_level_order(sol.buildTree([1, 2, 3], [3, 2, 1])) == [1, None, 2, None, 3]
assert get_level_order(sol.buildTree([1, 2, 3], [1, 3, 2])) == [2, 1, 3]
assert get_level_order(sol.buildTree([2, 3, 1], [3, 2, 1])) == [1, 2, None, None, 3]
assert get_level_order(sol.buildTree([1, 2, 3], [2, 3, 1])) == [1, None, 3, 2]

assert get_level_order(sol.buildTree([0, 1, 2, 3, 4, 5, 6], [0, 2, 1, 4, 6, 5, 3])) == [
    3,
    1,
    5,
    0,
    2,
    4,
    6,
]

assert get_level_order(
    sol.buildTree([4, 2, 5, 1, 6, 3], [4, 5, 2, 6, 3, 1])
) == [1, 2, 3, 4, 5, 6]

assert get_level_order(
    sol.buildTree([-3000, -1, 0, 3000], [-3000, -1, 3000, 0])
) == [0, -1, 3000, -3000]

assert get_level_order(sol.buildTree([-3000, 3000], [3000, -3000])) == [
    -3000,
    None,
    3000,
]

_inorder_in = [9, 3, 15, 20, 7]
_postorder_in = [9, 15, 7, 20, 3]
sol.buildTree(_inorder_in, _postorder_in)
assert _inorder_in == [9, 3, 15, 20, 7]
assert _postorder_in == [9, 15, 7, 20, 3]


def collect_inorder(node, out):
    if node is not None:
        collect_inorder(node.left, out)
        out.append(node.val)
        collect_inorder(node.right, out)
    return out


def collect_postorder(node, out):
    if node is not None:
        collect_postorder(node.left, out)
        collect_postorder(node.right, out)
        out.append(node.val)
    return out


def make_rng(seed):
    state = [seed]

    def nxt(modulus):
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return (state[0] >> 16) % modulus

    return nxt


def make_tree(vals, nxt):
    if not vals:
        return None
    i = nxt(len(vals))
    node = TreeNode(vals[i])
    node.left = make_tree(vals[:i], nxt)
    node.right = make_tree(vals[i + 1 :], nxt)
    return node


for seed in range(1, 40):
    nxt = make_rng(seed)
    vals = list(range(-6, 7))
    tree = make_tree(vals, nxt)
    ino = collect_inorder(tree, [])
    post = collect_postorder(tree, [])
    assert ino == vals
    built = sol.buildTree(ino, post)
    assert collect_inorder(built, []) == ino
    assert collect_postorder(built, []) == post
    assert get_level_order(built) == get_level_order(tree)

chain_inorder = list(range(200))
chain_postorder = list(range(200))
expected_chain = [199]
for v in range(198, -1, -1):
    expected_chain.append(v)
    expected_chain.append(None)
while expected_chain and expected_chain[-1] is None:
    expected_chain.pop()
assert get_level_order(sol.buildTree(chain_inorder, chain_postorder)) == expected_chain

right_chain_inorder = list(range(200))
right_chain_postorder = list(range(199, -1, -1))
expected_right_chain = [0]
for v in range(1, 200):
    expected_right_chain.append(None)
    expected_right_chain.append(v)
assert (
    get_level_order(sol.buildTree(right_chain_inorder, right_chain_postorder))
    == expected_right_chain
)


def balanced_postorder(lo, hi, out):
    if lo > hi:
        return out
    mid = (lo + hi) // 2
    balanced_postorder(lo, mid - 1, out)
    balanced_postorder(mid + 1, hi, out)
    out.append(mid)
    return out


big_inorder = list(range(1023))
big_postorder = balanced_postorder(0, 1022, [])
big_tree = sol.buildTree(big_inorder, big_postorder)
assert collect_inorder(big_tree, []) == big_inorder
assert collect_postorder(big_tree, []) == big_postorder
assert big_tree.val == 511
assert big_tree.left.val == 255
assert big_tree.right.val == 767
assert len(get_level_order(big_tree)) == 1023