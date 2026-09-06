"""
DRILL: Bundle Refunds
TRAINS: recursive-descent

A warehouse settles its account as one long string of credits and debits,
e.g. "12-(3+4-(2))". Related items are grouped in parentheses: a bundle
is bought or refunded as a whole, and bundles nest. The auditors want the
account filed as a tree: amounts are leaves, each '+' or '-' is a node
with everything settled so far on the left and the newest part on the
right, and a bundle hangs off its operator as a single subtree.

Build the tree and return its root.

Already installed (inherited from dsa.recursive_descent.Parser): `number`
reads a digit run into a TreeNode leaf, and `expr` chains parts with '+'
and '-' - but `expr` doesn't fetch its parts itself, it calls `atom` for
each one. You write `atom` and nothing else.

The grammar:

    expr   := atom (('+' | '-') atom)*
    atom   := number | '(' expr ')'
    number := digit+        (already installed)

Example:

Input: S = "12-(3+4)"
Output: the root of

      [-]
   ┌───┴───┐
  [12]    [+]
        ┌──┴──┐
       [3]   [4]

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+', '-', '(' and ')'. No spaces.
    Parentheses are balanced; every bundle and the whole string start
    with a number or a '('.

    REQUIRED: `atom` peeks at one character and consumes exactly one
    part - a plain amount or a whole bundle - leaving the cursor just
    past what it consumed, ')' included.

---

Learning.

"""

from dsa.recursive_descent import Parser


class Solution(Parser):
    def atom(self) -> TreeNode:
        if self.curr == "(":
            self.advance()
            val = self.expr()
            self.advance()
            return val
        return self.number()


p = Solution("12-(3+4)")
t = p.expr()

draw_tree(t)

assert t.val == "-"
assert t.left.val == 12
assert t.right.val == "+"
assert t.right.left.val == 3 and t.right.right.val == 4
assert p.i == len(p.S)

p = Solution("12-(3+4-(2))")
t = p.expr()
assert t.val == "-"
assert t.left.val == 12
inner = t.right
assert inner.val == "-" and inner.right.val == 2
assert inner.left.val == "+"
assert inner.left.left.val == 3 and inner.left.right.val == 4

p = Solution("((7))")
t = p.expr()
assert t.val == 7 and t.left is None and t.right is None
assert p.i == len(p.S)

p = Solution("10-(2+3)+1")
t = p.expr()
assert t.val == "+" and t.right.val == 1
assert t.left.val == "-" and t.left.left.val == 10
assert t.left.right.val == "+"
assert t.left.right.left.val == 2 and t.left.right.right.val == 3

p = Solution("42")
t = p.expr()
assert t.val == 42 and t.left is None and t.right is None
