# REFERENCE: d335 Decrypt Message
class Solution:
    def decrypt(self, word):
        prev = 1
        out = []
        for c in word:
            v = (ord(c) - prev - 97) % 26 + 97
            out.append(chr(v))
            prev += v
        return ''.join(out)
