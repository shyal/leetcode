# REFERENCE: d159 Exclusive From Call Tree
def exclusive(n: int, root: Node) -> [int]
  ret res = table(n)
  def visit(node)
    if node is not root
      inside = sum for child in node.children.values(): child.val["dur"]
      res[node.val["id"]] += node.val["dur"] - inside
    for child in node.children.values()
      visit(child)
  visit(root)
