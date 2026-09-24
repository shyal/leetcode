# REFERENCE: d66 Ledger Tally
def tally(S: str) -> int
  total, num, sign = 0, 0, 1
  for ch in S
    if ch.isdigit()
      num = num * 10 + int(ch)
    else
      total += sign * num
      num, sign = 0, 1 if ch == "+" else -1
  total + sign * num
