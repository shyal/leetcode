# REFERENCE: d505 EPI 15.9 Generate binary trees
class Solution:
    def generate_all_binary_trees(self, num_nodes):
        if num_nodes == 0:
            return [None]
        out = []
        for left in range(num_nodes):
            for l in self.generate_all_binary_trees(left):
                for r in self.generate_all_binary_trees(num_nodes - 1 - left):
                    out.append(TreeNode(0, l, r))
        return out
