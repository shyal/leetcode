# REFERENCE: d74 All Substrings
def allSubstrings(s: str) -> [str]
  [s[i:j] for i in 0..<len(s) for j in i + 1..len(s)]
