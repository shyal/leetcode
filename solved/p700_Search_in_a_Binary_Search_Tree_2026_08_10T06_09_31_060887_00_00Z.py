"""
URL: https://leetcode.com/problems/search-in-a-binary-search-tree/description/?envType=problem-list-v2&envId=vn57k9wr

700. Search in a Binary Search Tree

You are given the root of a binary search tree (BST) and an integer val.

Find the node in the BST that the node's value equals val and return the
subtree rooted with that node. If such a node does not exist, return null.


Example 1:

Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]

Example 2:

Input: root = [4,2,7,1,3], val = 5
Output: []


Constraints:

    The number of nodes in the tree is in the range [1, 5000].
    1 <= Node.val <= 10^7
    root is a binary search tree.
    1 <= val <= 10^7
"""


class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        def find(root):
            if root:
                if root.val == val:
                    return root
                elif val < root.val:
                    return find(root.left)
                else:
                    return find(root.right)
        return find(root)

sol = Solution()

draw_tree(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 2))  # [2, 1, 3]

assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 2)) == [2, 1, 3]
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 5)) == []
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 4)) == [4, 2, 7, 1, 3]
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 7)) == [7]
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 1)) == [1]
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 3)) == [3]
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 6)) == []
assert get_level_order(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 8)) == []
assert get_level_order(sol.searchBST(build_tree([1]), 1)) == [1]
assert get_level_order(sol.searchBST(build_tree([1]), 2)) == []
assert get_level_order(sol.searchBST(build_tree([10000000]), 10000000)) == [10000000]
assert get_level_order(sol.searchBST(build_tree([10000000]), 1)) == []
assert (
    get_level_order(
        sol.searchBST(build_tree([8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]), 4)
    )
    == [4, 2, 6, 1, 3, 5, 7]
)
assert (
    get_level_order(
        sol.searchBST(build_tree([8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]), 12)
    )
    == [12, 10, 14, 9, 11, 13, 15]
)
assert (
    get_level_order(
        sol.searchBST(build_tree([8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]), 15)
    )
    == [15]
)
assert (
    get_level_order(
        sol.searchBST(build_tree([8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]), 16)
    )
    == []
)