# REFERENCE: d329 Balanced Tree
class Solution:
    def is_balanced(self, node):
        def height(n):
            if n is None:
                return 0
            left, right = height(n.left), height(n.right)
            if left == -1 or right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(node) != -1
