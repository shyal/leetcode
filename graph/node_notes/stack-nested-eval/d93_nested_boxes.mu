# REFERENCE: d93 Nested Boxes
def weight(s: str) -> int
  stack = [0]
  for ch in s
    if ch == "("
      stack <- 0
    elif ch == ")"
      w = stack .
      stack[-1] += 2 * w
    else
      stack[-1] += int(ch)
  stack[0]
