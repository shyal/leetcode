"""
Given the root rootNode of a binary search tree with nonnegative keys
and an integer num, return the largest key in the tree that is smaller
than num. Return -1 when no key is smaller than num.

Example 1:

Input: rootNode = the root of

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

       num = 17
Output: 14
Explanation: the keys smaller than 17 are 5, 9, 11, 12 and 14.

Example 2:

Input: rootNode = the root of

        10
       /  \\
      6    18
     / \\   / \\
    4   8 15  21

       num = 10
Output: 8
Explanation: a key equal to num is not smaller than num.

Example 3:

Input: rootNode = the root of the tree of Example 2, num = 4
Output: -1

Constraints:

    0 <= number of nodes <= 10^4
    0 <= key <= 10^9
    The keys are distinct.
    0 <= num <= 10^9

    REQUIRED: O(h) time, where h is the height of the tree, O(1) extra
    space. NO traversal of the whole tree, NO list of the keys.
"""


class Solution:
    def find_largest_smaller_key(self, rootNode: TreeNode | None, num: int) -> int:
        pass


sol = Solution()

root = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(root)
print(sol.find_largest_smaller_key(root, 17))  # 14

# assert sol.find_largest_smaller_key(build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14]), 17) == 14
# assert sol.find_largest_smaller_key(build_tree([10, 6, 18, 4, 8, 15, 21]), 10) == 8
# assert sol.find_largest_smaller_key(build_tree([10, 6, 18, 4, 8, 15, 21]), 4) == -1
# assert sol.find_largest_smaller_key(build_tree([10, 6, 18, 4, 8, 15, 21]), 22) == 21
# assert sol.find_largest_smaller_key(build_tree([10, 6, 18, 4, 8, 15, 21]), 6) == 4
# assert sol.find_largest_smaller_key(build_tree([8, 5, 9, 4, 7, None, 11, 1, None, None, None, None, 12, None, 3, None, None, 2]), 11) == 9
# assert sol.find_largest_smaller_key(build_tree([8, 5, 9, 4, 7, None, 11, 1, None, None, None, None, 12, None, 3, None, None, 2]), 1) == -1
# assert sol.find_largest_smaller_key(build_tree([8, 5, 9, 4, 7, None, 11, 1, None, None, None, None, 12, None, 3, None, None, 2]), 3) == 2
# assert sol.find_largest_smaller_key(build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14]), 12) == 11
# assert sol.find_largest_smaller_key(build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14]), 1000) == 25
# assert sol.find_largest_smaller_key(build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14]), 0) == -1
# assert sol.find_largest_smaller_key(None, 5) == -1
# assert sol.find_largest_smaller_key(build_tree([5]), 5) == -1
# assert sol.find_largest_smaller_key(build_tree([5]), 6) == 5
# assert sol.find_largest_smaller_key(build_tree([0]), 0) == -1
# assert sol.find_largest_smaller_key(build_tree([10 ** 9]), 10 ** 9) == -1
# chain = reduce(lambda t, k: TreeNode(k, t, None), range(1, 10 ** 4), TreeNode(0))
# assert sol.find_largest_smaller_key(chain, 1) == 0
# assert sol.find_largest_smaller_key(chain, 0) == -1
# assert sol.find_largest_smaller_key(chain, 5000) == 4999
# assert sol.find_largest_smaller_key(chain, 10 ** 4) == 10 ** 4 - 1
