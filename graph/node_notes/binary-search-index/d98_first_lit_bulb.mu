# REFERENCE: d98 First Lit Bulb
class Solution
  def firstLit(lit: [bool]) -> int
    first i in 0..<len(lit) if lit[i]
