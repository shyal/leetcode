"""
EPI 14.2 Find the first key greater than a given value in a BST

Given tree, the root of a binary search tree, and an integer k, return the
node with the smallest key that is greater than k. When several nodes
hold that key, return the first of them in inorder. Return None when no
key is greater than k.

Example 1:

Input: tree = [20, 9, 25, 5, 12, None, None, None, None, 11, 14], k = 9
Output: the node 11
Explanation: the keys greater than 9 are 11, 12, 14, 20, 25.

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: the same tree, k = 14
Output: the node 20

Example 3:

Input: the same tree, k = 25
Output: None

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= node.val, k <= 10^9
    The tree satisfies the BST property: left keys <= node key <= right
    keys.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO
    list of the keys. NO recursion.
"""


class Solution:
    def find_first_greater_than_k(self, tree: TreeNode | None, k: int) -> TreeNode | None:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.find_first_greater_than_k(t, 9).val)  # 11

# assert sol.find_first_greater_than_k(t, 9) is find_node(t, 11)
# assert sol.find_first_greater_than_k(t, 14) is t
# assert sol.find_first_greater_than_k(t, 25) is None
# assert sol.find_first_greater_than_k(t, 4) is find_node(t, 5)
# assert sol.find_first_greater_than_k(t, 13) is find_node(t, 14)
# assert sol.find_first_greater_than_k(t, 20) is find_node(t, 25)
# assert sol.find_first_greater_than_k(t, 30) is None
# assert sol.find_first_greater_than_k(t, -10 ** 9).val == 5
# assert sol.find_first_greater_than_k(None, 0) is None
# assert sol.find_first_greater_than_k(build_tree([3]), 2).val == 3
# assert sol.find_first_greater_than_k(build_tree([3]), 3) is None
# t = build_tree([5, 3, 7, 3, 5, 7])
# assert sol.find_first_greater_than_k(t, 3) is t.left.right
# assert sol.find_first_greater_than_k(t, 4) is t.left.right
# assert sol.find_first_greater_than_k(t, 5) is t.right.left
# chain = build_tree([4999] + [v for k in range(4998, -1, -1) for v in (k, None)])
# assert sol.find_first_greater_than_k(chain, 0).val == 1
# assert sol.find_first_greater_than_k(chain, 4998).val == 4999
# keys = [(2 * p + 1) * 2 ** (15 - d) - 1 for d in range(16) for p in range(2 ** d)]
# big = build_tree(keys)
# assert sol.find_first_greater_than_k(big, 12345).val == 12346
# assert sol.find_first_greater_than_k(big, 2 ** 16 - 2) is None
