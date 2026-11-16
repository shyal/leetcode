# REFERENCE: d545 Maximum Sum With No Parent And Child
class Solution:
    def maxSum(self, root):
        def both(node):
            if not node:
                return 0, 0
            (ls, lt), (rs, rt) = both(node.left), both(node.right)
            return max(ls, lt) + max(rs, rt), node.val + ls + rs

        return max(both(root))
