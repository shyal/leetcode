"""
URL: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/?envType=problem-list-v2&envId=vn57k9wr

105. Construct Binary Tree from Preorder and Inorder Traversal

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

Example 1:

Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]

Constraints:

    1 <= preorder.length <= 3000
    inorder.length == preorder.length
    -3000 <= preorder[i], inorder[i] <= 3000
    preorder and inorder consist of unique values.
    Each value of inorder also appears in preorder.
    preorder is guaranteed to be the preorder traversal of the tree.
    inorder is guaranteed to be the inorder traversal of the tree.

---


       3
     .   .
    9    20
        .  .
       15   7

preorder  =  3, 9, 20, 15, 7
inorder   =  9, 3, 15, 20, 7

With pre, the root is 3, so we can get the number of left nodes by counting the
number nodes, left of 3 in the post, and the number of right nodes by counting
the number of nodes to the right of 3 in the post

LEETCODE: Accepted (67 ms, 90.7 MB)
"""


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if preorder == inorder == []:
            return None
        root = preorder[0]
        inorder_root_index = inorder.index(root)
        inorder_left = inorder[:inorder_root_index]
        return TreeNode(
            val=root,
            left=self.buildTree(preorder[1 : len(inorder_left) + 1], inorder_left),
            right=self.buildTree(
                preorder[len(inorder_left) + 1 :], inorder[inorder_root_index + 1 :]
            ),
        )


sol = Solution()

# Example 1
root1 = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(root1)
print(get_level_order(root1))  # [3,9,20,None,None,15,7]

# Example 2
root2 = sol.buildTree([-1], [-1])
print(get_level_order(root2))  # [-1]

assert get_level_order(sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [
    3,
    9,
    20,
    None,
    None,
    15,
    7,
]
assert get_level_order(sol.buildTree([-1], [-1])) == [-1]

assert get_level_order(sol.buildTree([], [])) == []
assert get_level_order(sol.buildTree([1], [1])) == [1]
assert get_level_order(sol.buildTree([1, 2], [2, 1])) == [1, 2]
assert get_level_order(sol.buildTree([1, 2], [1, 2])) == [1, None, 2]
assert get_level_order(sol.buildTree([-3000], [-3000])) == [-3000]
assert get_level_order(
    sol.buildTree([i for i in range(1, 11)], [i for i in range(1, 11)])
) == [
    1,
    None,
    2,
    None,
    3,
    None,
    4,
    None,
    5,
    None,
    6,
    None,
    7,
    None,
    8,
    None,
    9,
    None,
    10,
]
assert get_level_order(
    sol.buildTree([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
) == [10, 9, None, 8, None, 7, None, 6, None, 5, None, 4, None, 3, None, 2, None, 1]
assert get_level_order(
    sol.buildTree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
) == [1, 2, None, 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9, None, 10]
assert get_level_order(sol.buildTree([1, 2, 3, 4, 5], [3, 2, 4, 1, 5])) == [
    1,
    2,
    5,
    3,
    4,
]
assert get_level_order(sol.buildTree([2, 1, 3], [1, 2, 3])) == [2, 1, 3]
assert get_level_order(sol.buildTree([2, 3, 1], [3, 2, 1])) == [2, 3, 1]
