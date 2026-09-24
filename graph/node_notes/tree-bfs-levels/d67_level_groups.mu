# REFERENCE: d67 Level Groups
def levelGroups(tree: list) -> [[int]]
  q = deque([tree])
  out = []
  for (_, level) in levels(q, grouped = true)
    out <- [node[0] for node in level]
    for node in level
      q.extend(node[1:])
  out
