# REFERENCE: d424 EPI 8.2 Evaluate RPN expressions
class Solution
  def evaluate(expression: str) -> int
    apply = {
      '+': (a, b) -> a + b,
      '-': (a, b) -> a - b,
      '*': (a, b) -> a * b,
      '/': (a, b) -> int(a / b),
    }
    stack = []
    for token in expression.split(',')
      if token in apply
        b, a = stack.pop(), stack.pop()
        stack <- apply[token](a, b)
      else
        stack <- int(token)
    stack[-1]
