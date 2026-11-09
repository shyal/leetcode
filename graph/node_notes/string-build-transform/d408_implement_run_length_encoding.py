# REFERENCE: d408 EPI 6.11 Implement run-length encoding
class Solution:
    def encoding(self, s):
        out, i = [], 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            out.append(str(j - i) + s[i])
            i = j
        return "".join(out)

    def decoding(self, s):
        out, count = [], 0
        for c in s:
            if c.isdigit():
                count = count * 10 + int(c)
            else:
                out.append(c * count)
                count = 0
        return "".join(out)
