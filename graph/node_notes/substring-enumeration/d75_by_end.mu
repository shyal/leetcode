# REFERENCE: d75 Substrings by End
def substringsByEnd(s: str) -> [str]
  [s[i:j + 1] for j in 0..<len(s) for i in 0..j]
