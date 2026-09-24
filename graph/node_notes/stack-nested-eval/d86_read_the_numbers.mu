# REFERENCE: d86 Read The Numbers
def getNumbers(s: str) -> [int]
  out, num = [], 0
  for ch in s
    if ch == "+"
      out <- num
      num = 0
    else
      num = num * 10 + int(ch)
  out + [num]
