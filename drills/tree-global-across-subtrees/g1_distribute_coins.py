"""
DRILL: Distribute Coins
TRAINS: tree-global-across-subtrees

Given the root of a binary tree with n nodes, return the minimum number
of moves that leaves exactly one coin on every node. Each node holds
Node.val coins, and the whole tree holds n coins. In one move you
transfer one coin between two nodes joined by an edge.

Example 1:

Input: root = [3, 0, 0]
Output: 2
Explanation: one coin moves from the root to each child.

Example 2:

Input: root = [0, 3, 0]
Output: 3
Explanation: two coins move from the left child to the root, then one
moves from the root to the right child.

Example 3:

Input: root = [1, 0, 0, None, 3]
Output: 4
Explanation: coins travel one edge at a time, so a coin two edges from
its target costs two moves.

Constraints:

    1 <= n <= 100
    0 <= Node.val <= n
    The values across the tree sum to n.

    REQUIRED: one pass, O(n). The move total must accumulate outside
    the recursion's returns. Sending the move count up in place of what
    the parent needs is the failure mode this drill exists to kill. NO
    tuple returns bundling the total, NO second traversal.
"""


class Solution:
    def distributeCoins(self, root: Optional[TreeNode]) -> int:
        pass


sol = Solution()

tree = build_tree([0, 3, 0])
draw_tree(tree)

print(sol.distributeCoins(tree))  # 3

# assert sol.distributeCoins(build_tree([3, 0, 0])) == 2
# assert sol.distributeCoins(build_tree([0, 3, 0])) == 3
# assert sol.distributeCoins(build_tree([1, 0, 2])) == 2
# assert sol.distributeCoins(build_tree([1, 0, 0, None, 3])) == 4
# assert sol.distributeCoins(build_tree([1])) == 0
# assert sol.distributeCoins(build_tree([2, 0, 0, 2])) == 2
# assert sol.distributeCoins(build_tree([4, 0, 0, 0])) == 4
# assert sol.distributeCoins(build_tree([0, None, 0, None, 3])) == 3
