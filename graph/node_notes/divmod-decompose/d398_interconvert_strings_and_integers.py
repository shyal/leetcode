# REFERENCE: d398 EPI 6.1 Interconvert strings and integers
class Solution:
    def int_to_string(self, x):
        sign, x = ("-" if x < 0 else ""), abs(x)
        out = []
        while True:
            x, d = divmod(x, 10)
            out.append(chr(ord("0") + d))
            if x == 0:
                break
        return sign + "".join(reversed(out))

    def string_to_int(self, s):
        n = 0
        for c in s[s[0] in "+-" :]:
            n = n * 10 + ord(c) - ord("0")
        return -n if s[0] == "-" else n
