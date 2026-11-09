# REFERENCE: d424 EPI 8.2 Evaluate RPN expressions
class Solution:
    def evaluate(self, expression):
        apply = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),
        }
        stack = []
        for token in expression.split(","):
            if token in apply:
                b, a = stack.pop(), stack.pop()
                stack.append(apply[token](a, b))
            else:
                stack.append(int(token))
        return stack[-1]
