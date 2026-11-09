# REFERENCE: d498 EPI 15.2 Compute all mnemonics for a phone number
class Solution:
    def phone_mnemonic(self, phone_number):
        keys = ["0", "1", "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"]
        out, word = [], []

        def spell(i):
            if i == len(phone_number):
                out.append("".join(word))
                return
            for c in keys[int(phone_number[i])]:
                word.append(c)
                spell(i + 1)
                word.pop()

        spell(0)
        return out
