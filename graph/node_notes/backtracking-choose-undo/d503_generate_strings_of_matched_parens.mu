# REFERENCE: d503 EPI 15.7 Generate strings of matched parens
class Solution
  def generate_balanced_parentheses(num_pairs: int) -> [str]
    ret out, s = []..
    def extend(opened, closed)
      if closed == num_pairs
        out <- "".join(s)
        return
      if opened < num_pairs
        s <- "("
        extend(opened + 1, closed)
        s .
      if closed < opened
        s <- ")"
        extend(opened, closed + 1)
        s .
    extend(0, 0)
