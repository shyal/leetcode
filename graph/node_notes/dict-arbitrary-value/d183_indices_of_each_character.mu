# REFERENCE: d183 Indices Of Each Character
class Solution
  def indices(s: str) -> {char: [int]}
    {:list: c <- i for ~i, c in s}
