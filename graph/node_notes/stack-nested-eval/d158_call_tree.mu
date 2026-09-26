# REFERENCE: d158 Call Tree
def callTree(events: [(int, str, int)]) -> Node
  ret root = Node({})
  stack = [root]
  for (id, op, t) in events
    if op == "start"
      stack <- Node({"id": id, "start": t}, parent=stack[-1])
    else
      node = stack .
      node.val["dur"] = t - node.val["start"] + 1
