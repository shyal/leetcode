# REFERENCE: d504 EPI 15.8 Generate palindromic decompositions
class Solution:
    def palindrome_decompositions(self, text):
        out, parts = [], []

        def cut(start):
            if start == len(text):
                out.append(parts[:])
                return
            for end in range(start + 1, len(text) + 1):
                piece = text[start:end]
                if piece == piece[::-1]:
                    parts.append(piece)
                    cut(end)
                    parts.pop()

        cut(0)
        return out
