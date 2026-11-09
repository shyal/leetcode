# REFERENCE: d507 EPI 15.11 Compute a Gray code
class Solution:
    def gray_code(self, num_bits):
        codes = [0]
        for bit in range(num_bits):
            codes += [x | 1 << bit for x in reversed(codes)]
        return codes
