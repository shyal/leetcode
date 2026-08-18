"""
DRILL: Number Scanner
TRAINS: recursive-descent

An old sorting machine reads shipping labels with a mechanical head that
slides along the label one character at a time. Labels mix amounts with
punctuation, like "120+45-30". You are rebuilding the head.

The head is a class: it holds the label S and its position i, starting at
0. It has one skill, `number`: called while parked on a digit, it reads
the full amount under it - one digit at a time, building up the value as
it slides - and comes to rest exactly on the first character that is not
a digit (or the end of the label). It hands back the amount as a TreeNode
leaf, a part the rest of the machine will later assemble into bigger
things.

The grammar it implements:

    number := digit+

Constraints:

    S contains digits and other characters.
    No int() on slices, no regex - the head sees one character at a time.
    The tests slide the head across a label and check both the amounts
    returned and where the head comes to rest.

---

Assisted solve (learning).

"""


class Solution:
    def __init__(self, S: str) -> None:
        self.S, self.i = S, 0

    def number(self) -> TreeNode:
        n = 0
        while self.i < len(self.S) and self.S[self.i].isdigit():
            n = n * 10 + int(self.S[self.i])
            self.i += 1
        return TreeNode(n)
            


p = Solution("120+45-30")

t = p.number()
draw_tree(t)

assert t.val == 120
assert p.i == 3 and p.S[p.i] == "+"
p.i += 1
assert p.number().val == 45
assert p.S[p.i] == "-"
p.i += 1
assert p.number().val == 30
assert p.i == len(p.S)

p = Solution("7")
assert p.number().val == 7
assert p.i == 1

p = Solution("999999+1")
assert p.number().val == 999999
assert p.S[p.i] == "+"

print("All tests passed!")

