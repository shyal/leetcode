# REFERENCE: d159 Exclusive From Call Tree
def exclusive(n: int, root: Node) -> [int]
  ret res = table(n)
  def visit(node)
    for child in node.children.values()
      res[child.val["id"]] += child.val["dur"]
      if node is not root
        res[node.val["id"]] -= child.val["dur"]
      visit(child)
  visit(root)
