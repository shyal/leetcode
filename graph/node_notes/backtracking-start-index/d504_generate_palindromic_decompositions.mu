# REFERENCE: d504 EPI 15.8 Generate palindromic decompositions
class Solution
  def palindrome_decompositions(text: str) -> [[str]]
    ret out, parts = []..
    def cut(start)
      if start == len(text)
        out <- parts[:]
        return
      for end in start + 1..len(text)
        piece = text[start:end]
        if piece == piece[::-1]
          parts <- piece
          cut(end)
          parts .
    cut(0)
