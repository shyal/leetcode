# REFERENCE: d399 EPI 6.2 Base conversion
class Solution:
    def convert_base(self, num_as_string, b1, b2):
        DIGITS = "0123456789ABCDEF"
        negative = num_as_string[0] == "-"
        n = 0
        for c in num_as_string[negative:]:
            n = n * b1 + DIGITS.index(c)
        out = []
        while True:
            n, d = divmod(n, b2)
            out.append(DIGITS[d])
            if n == 0:
                break
        return "-" * negative + "".join(reversed(out))
