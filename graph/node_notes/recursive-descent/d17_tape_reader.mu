# REFERENCE: d17 Tape Reader
from dsa.recursive_descent import Parser

class Solution extends Parser
  def expr() -> TreeNode
    val = self.number()
    while not self.ended and self.curr in "+-"
      val = TreeNode(left = val, val = self.next, right = self.number())
    val
