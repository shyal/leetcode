"""
URL: https://leetcode.com/problems/increasing-order-search-tree/description/?envType=problem-list-v2&envId=vn57k9wr

897. Increasing Order Search Tree

Given the root of a binary search tree, rearrange the tree in in-order so that the leftmost node in the tree is now the root of the tree, and every node has no left child and only one right child.

Example 1:

Input: root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
Output: [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]

Example 2:

Input: root = [5,1,7]
Output: [1,null,5,null,7]

Constraints:

    The number of nodes in the given tree will be in the range [1, 100].
    0 <= Node.val <= 1000
"""


class Solution:
    def increasingBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            nodes.append(node)
            dfs(node.right)

        nodes = []
        dfs(root)
        for i in range(len(nodes)):
            nodes[i].left = None
            nodes[i].right = nodes[i + 1] if i + 1 < len(nodes) else None
        return nodes[0]


sol = Solution()

# print(
#     get_level_order(
#         sol.increasingBST(
#             build_tree([5, 3, 6, 2, 4, None, 8, 1, None, None, None, 7, 9])
#         )
#     )
# )  # [1,None,2,None,3,None,4,None,5,None,6,None,7,None,8,None,9]

assert get_level_order(
    sol.increasingBST(build_tree([5, 3, 6, 2, 4, None, 8, 1, None, None, None, 7, 9]))
) == [1, None, 2, None, 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9]

assert get_level_order(sol.increasingBST(build_tree([5, 1, 7]))) == [
    1,
    None,
    5,
    None,
    7,
]
assert get_level_order(sol.increasingBST(build_tree([1]))) == [1]
assert get_level_order(sol.increasingBST(build_tree([0]))) == [0]
assert get_level_order(sol.increasingBST(build_tree([1000]))) == [1000]
assert get_level_order(sol.increasingBST(build_tree([2, 1]))) == [1, None, 2]
assert get_level_order(sol.increasingBST(build_tree([1, None, 2]))) == [1, None, 2]
assert get_level_order(sol.increasingBST(build_tree([3, 2, None, 1]))) == [
    1,
    None,
    2,
    None,
    3,
]
# assert get_level_order(sol.increasingBST(build_tree([1, None, 3, None, 2]))) == [
#     1,
#     None,
#     2,
#     None,
#     3,
# ]
assert get_level_order(sol.increasingBST(build_tree([4, 2, 5, 1, 3]))) == [
    1,
    None,
    2,
    None,
    3,
    None,
    4,
    None,
    5,
]
