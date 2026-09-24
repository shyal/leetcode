# REFERENCE: d87 Read The Signed Numbers
def getPositiveAndNegativeNumbers(s: str) -> [int]
  out, num, sign = [], 0, 1
  for ch in s
    if ch.isdigit()
      num = num * 10 + int(ch)
    else
      out <- sign * num
      num, sign = 0, 1 if ch == "+" else -1
  out + [sign * num]
