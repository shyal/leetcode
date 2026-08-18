"""
DRILL: Tape Reader
TRAINS: recursive-descent

At closing time a shopkeeper's register prints one long paper tape: every
sale and refund of the day glued into a single string, e.g. "120+45-30".
Head office doesn't want a bare total - they want the working itself,
filed as a tree they can audit joint by joint.

Turn the tape into that tree and return its root. Every amount is a leaf.
Every operator becomes an inner node whose left child is everything
assembled so far and whose right child is the amount just read, so the
tree leans left exactly like the tape reads.

The reading head already exists: `number` (inherited from
dsa.recursive_descent.Parser) slides the cursor over a digit run and
hands back the amount as a TreeNode leaf. You write `expr` and nothing
else.

The grammar:

    expr   := number (('+' | '-') number)*
    number := digit+        (already installed)

Example:

Input: S = "120+45-30"
Output: the root of

          [-]
       ┌───┴──┐
      [+]    [30]
     ┌─┴──┐
    [120] [45]

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+' and '-'. No spaces.
    S starts with a digit; operators are always followed by a number.

    REQUIRED: `expr` never touches a digit - every amount is read by
    calling self.number(). One loop: read the operator, read the next
    amount, weld a new operator node with the tree so far on the left
    and the fresh leaf on the right. When the tape ends the cursor is
    at len(S) and the last node welded is the root.
"""

from dsa.recursive_descent import Parser


class Solution(Parser):
    def expr(self) -> TreeNode:
        pass


p = Solution("120+45-30")
t = p.expr()

draw_tree(t)

assert t.val == "-"
assert t.right.val == 30 and t.right.left is None
assert t.left.val == "+"
assert t.left.left.val == 120 and t.left.right.val == 45
assert p.i == len(p.S)

p = Solution("7")
t = p.expr()
assert t.val == 7 and t.left is None and t.right is None

p = Solution("10-100+1000")
t = p.expr()
assert t.val == "+" and t.right.val == 1000
assert t.left.val == "-"
assert t.left.left.val == 10 and t.left.right.val == 100

p = Solution("1+2+3+4")
t = p.expr()
assert t.val == "+" and t.right.val == 4
assert t.left.val == "+" and t.left.right.val == 3
assert t.left.left.val == "+"
assert t.left.left.left.val == 1 and t.left.left.right.val == 2

print("All tests passed!")
