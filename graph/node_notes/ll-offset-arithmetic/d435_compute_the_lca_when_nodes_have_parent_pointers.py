# REFERENCE: d435 EPI 9.4 Compute the LCA when nodes have parent pointers
class Solution:
    def lca(self, node0, node1):
        def depth(node):
            d = 0
            while node.parent:
                node, d = node.parent, d + 1
            return d

        d0, d1 = depth(node0), depth(node1)
        if d0 < d1:
            node0, node1, d0, d1 = node1, node0, d1, d0
        for _ in range(d0 - d1):
            node0 = node0.parent
        while node0 is not node1:
            node0, node1 = node0.parent, node1.parent
        return node0
