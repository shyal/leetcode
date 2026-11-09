# REFERENCE: d498 EPI 15.2 Compute all mnemonics for a phone number
class Solution
  def phone_mnemonic(phone_number: str) -> [str]
    keys = ["0", "1", "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"]
    ret out, word = []..
    def spell(i)
      if i == len(phone_number)
        out <- "".join(word)
        return
      for c in keys[int(phone_number[i])]
        word <- c
        spell(i + 1)
        word .
    spell(0)
