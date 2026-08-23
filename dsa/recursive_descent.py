class Parser:
    def __init__(self, S):
        self.S, self.i = S, 0

    def number(self):
        n = 0
        while not self.ended and self.S[self.i].isdigit():
            n = n * 10 + int(self.next)
        return TreeNode(n)

    def atom(self):
        if self.curr == "(":
            self.advance()
            val = self.expr()
            self.advance()
            return val
        return self.number()

    def term(self):
        val = self.atom()
        while not self.ended and self.curr in "*/":
            val = TreeNode(left=val, val=self.next, right=self.atom())
        return val

    def expr(self):
        val = self.term()
        while not self.ended and self.curr in "+-":
            val = TreeNode(left=val, val=self.next, right=self.term())
        return val

    def advance(self):
        self.i += 1

    @property
    def ended(self):
        return self.i == len(self.S)

    @property
    def curr(self):
        return self.S[self.i]

    @property
    def next(self):
        val = self.S[self.i]
        self.i += 1
        return val


class RecursiveDescent(Parser):
    def evaluate(self, node):
        if node.left is None:
            return node.val
        l, r = self.evaluate(node.left), self.evaluate(node.right)
        Op = {"+": add, "-": sub, "*": mul, "/": truediv}
        return Op[node.val](l, r)

    def draw(self, node):
        draw_tree(node)


if __name__ == "__main__":

    class Solution:
        def tally(self, S: str) -> int:
            rd = RecursiveDescent(S)
            tree = rd.expr()
            res = rd.evaluate(tree)
            rd.draw(tree)
            print("evaluates to:", res)
            return res

    sol = Solution()

    assert sol.tally("120+45-30") == 135
    assert sol.tally("3-9") == -6
    assert sol.tally("7") == 7
    assert sol.tally("10-100+1000") == 910
    assert sol.tally("5-3-3") == -1
    assert sol.tally("999999+1") == 1000000
    assert sol.tally("3*10") == 30
    assert sol.tally("10/2") == 5
    assert sol.tally("3*10+5") == 35

    print("All tests passed!")
