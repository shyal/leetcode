# REFERENCE: d376 EPI 4.10 Generate uniform random numbers
class Solution:
    def uniform_random(self, lower_bound, upper_bound):
        n = upper_bound - lower_bound + 1
        while True:
            r, size = 0, 1
            while size < n:
                r = (r << 1) | zero_one_random()
                size <<= 1
            if r < n:
                return lower_bound + r
