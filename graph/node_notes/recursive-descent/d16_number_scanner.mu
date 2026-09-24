# REFERENCE: d16 Number Scanner
def __init__(S: str) -> none
  self.S, self.i = S, 0

def number() -> TreeNode
  n = 0
  while self.i < len(self.S) and self.S[self.i].isdigit()
    n = n * 10 + int(self.S[self.i])
    self.i += 1
  TreeNode(n)
