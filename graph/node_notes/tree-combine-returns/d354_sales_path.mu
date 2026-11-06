# REFERENCE: d354 Sales Path
class Solution
  def get_cheapest_cost(rootNode: Node) -> int
    if not rootNode.children
      return rootNode.val
    cheapest = inf
    for child in rootNode.children
      cheapest = min(cheapest, self.get_cheapest_cost(child))
    rootNode.val + cheapest
