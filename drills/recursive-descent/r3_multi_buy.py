"""
DRILL: Multi-Buy
TRAINS: recursive-descent

A market stall totals an order given as one string, e.g. "2+3*4/6". The
operators '+' and '-' separate distinct items. The operators '*' and '/'
are multi-buys and per-unit splits inside a single item, so they bind
more tightly: "2+3*4" is an item of 2 plus an item of 3*4, never
(2+3)*4.

The stall files the order as a tree: amounts are leaves, operators are
inner nodes, and a run of '*' and '/' forms one subtree that hangs off
the surrounding '+' or '-'.

Build the tree and return its root.

Already installed (inherited from dsa.recursive_descent.Parser): `number`
reads a digit run into a TreeNode leaf, `atom` fetches one part, and
`expr` chains parts with '+' and '-'. But `expr` no longer asks `atom`
for its parts, it asks `term`. You write `term` and nothing else.

The grammar:

    expr   := term (('+' | '-') term)*
    term   := atom (('*' | '/') atom)*
    atom   := number        (already installed)
    number := digit+        (already installed)

Example:

Input: S = "2+3*4/6"
Output: the root of

      [+]
   ┌───┴───┐
  [2]     [/]
        ┌──┴──┐
       [*]   [6]
      ┌─┴─┐
     [3] [4]

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+', '-', '*' and '/'. No spaces.
    S starts with a digit; every operator is followed by a number.
    Runs of '*' and '/' associate left to right.

    REQUIRED: `term` never touches a digit - every part is fetched by
    calling self.atom(). One loop, claiming only '*' and '/': read the
    operator, read the next atom, weld a new operator node with the term
    so far on the left and the fresh atom on the right. `term` must stop
    the moment it sees '+', '-' or the end of the string, and leave that
    character unread. Consuming it is what makes the multi-buy swallow
    the rest of the order.
"""


from dsa.recursive_descent import Parser

class Solution(Parser):
    def term(self) -> TreeNode:
        pass

p = Solution("2+3*4/6")
t = p.expr()
draw_tree(t)
assert t.val == "+"
assert t.left.val == 2
assert t.right.val == "/" and t.right.right.val == 6
assert t.right.left.val == "*"
assert t.right.left.left.val == 3 and t.right.left.right.val == 4
assert p.i == len(p.S)

p = Solution("10-2*3")
t = p.expr()
assert t.val == "-" and t.left.val == 10
assert t.right.val == "*"
assert t.right.left.val == 2 and t.right.right.val == 3

p = Solution("100/10/5")
t = p.expr()
assert t.val == "/" and t.right.val == 5
assert t.left.val == "/"
assert t.left.left.val == 100 and t.left.right.val == 10

p = Solution("3*4-2*5")
t = p.expr()
assert t.val == "-"
assert t.left.val == "*" and t.left.left.val == 3 and t.left.right.val == 4
assert t.right.val == "*" and t.right.left.val == 2 and t.right.right.val == 5

p = Solution("7")
t = p.expr()
assert t.val == 7 and t.left is None and t.right is None

print("All tests passed!")
