class Parser:
    def __init__(self, S):
        self.S, self.i = S, 0

    def number(self):
        n = 0
        while self.i < len(self.S) and self.S[self.i].isdigit():
            n = n * 10 + int(self.S[self.i])
            self.i += 1
        return TreeNode(n)

    def atom(self):
        return self.number()

    def term(self):
        return self.atom()

    def expr(self):
        val = self.term()
        while self.i < len(self.S) and self.S[self.i] in "+-":
            op = self.S[self.i]
            self.i += 1
            rhs = self.term()
            node = TreeNode(op)
            node.left, node.right = val, rhs
            val = node
        return val

class RecursiveDescent(Parser):
    def evaluate(self, node):
        if node.left is None:
            return node.val
        l, r = self.evaluate(node.left), self.evaluate(node.right)
        return l + r if node.val == "+" else l - r

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

    print("All tests passed!")
