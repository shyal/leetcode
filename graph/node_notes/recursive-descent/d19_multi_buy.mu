# REFERENCE: d19 Multi-Buy
from dsa.recursive_descent import Parser
extends Parser

def term() -> TreeNode
  val = self.atom()
  while not self.ended and self.curr in "*/"
    val = TreeNode(left = val, val = self.next, right = self.atom())
  val
