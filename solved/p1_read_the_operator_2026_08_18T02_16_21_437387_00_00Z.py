"""
**DRILL: Multi-Buy**  
**Trains:** Recursive-descent parsing

A market stall totals a customer's order given as a single string, for example `"2+3*4/6"`.

- The operators `+` and `-` separate distinct items.  
- The operators `*` and `/` express multi-buys and per-unit splits *inside* a single item; they bind more tightly than `+` and `-`.  
  Consequently `"2+3*4"` is an item of 2 plus an item of `3*4`, never `(2+3)*4`.

The stall's ledger records the whole order as a binary tree:
- numeric amounts are leaves,
- operators are internal nodes,
- a multi-buy (a chain of `*` / `/`) forms a single subtree that is attached by a surrounding `+` or `-`.

Your task is to build that tree and return its root.

### Already provided (inherited from `dsa.recursive_descent.Parser`)
- `number` - reads a consecutive run of digits and returns a `TreeNode` leaf  
- `atom` - obtains one atomic part  
- `expr` - chains parts with `+` and `-`  

Between those two methods, `expr` asks `term` for each part.  
**You implement only `term`.**

### Grammar
expr  := term (('+' | '-') term)*
term  := atom (('*' | '/') atom)*
atom  := number          (already installed)
number := digit+         (already installed)

### Example
**Input:** `S = "2+3*4/6"`  

**Output:** the root of the tree  

      [+]
   ┌───┴───┐
  [2]     [/]
        ┌──┴──┐
       [*]   [6]
      ┌─┴─┐
     [3] [4]

### Constraints
- `1 ≤ len(S) ≤ 10⁵`
- `S` contains only digits, `+`, `-`, `*` and `/`. No spaces.
- `S` always starts with a digit; every operator is followed by a number.
- Chains of `*` and `/` associate left-to-right.

### Required implementation discipline for `term`
- Obtain every part by calling `self.atom()` (never read digits yourself).  
- Use a single loop that claims only `*` and `/`:  
  1. read the operator,  
  2. read the next atom,  
  3. create a new operator node whose left child is the term built so far and whose right child is the newly read atom.  
- The moment the next character is `+`, `-` or the end of the string, the term is complete—return it and leave the remaining input untouched.

---

Assisted solve (learning)

"""

from dsa.recursive_descent import Parser

class Solution(Parser):
    def term(self) -> TreeNode:
        val = self.atom()
        while not self.ended and self.curr in '*/':
            op = self.curr
            self.advance()
            val = TreeNode(left=val, val=op, right=self.atom())
        return val

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
