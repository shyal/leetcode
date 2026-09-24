# REFERENCE: d105 Last Off Bulb
def lastOff(lit: [bool]) -> int
  (first i in 0..<len(lit) if lit[i]) - 1
