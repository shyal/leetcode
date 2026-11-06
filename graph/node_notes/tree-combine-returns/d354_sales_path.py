# REFERENCE: d354 Sales Path
class Solution:
    def get_cheapest_cost(self, rootNode):
        if not rootNode.children:
            return rootNode.val
        cheapest = inf
        for child in rootNode.children:
            cheapest = min(cheapest, self.get_cheapest_cost(child))
        return rootNode.val + cheapest
