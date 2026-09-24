# REFERENCE: d18 Bundle Refunds
from dsa.recursive_descent import Parser
extends Parser

def atom() -> TreeNode
  if self.curr == "("
    self.advance()
    val = self.expr()
    self.advance()
    return val
  self.number()
