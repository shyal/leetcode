# REFERENCE: d481 EPI 13.8 Compute the union of intervals
class Solution:
    def union_of_intervals(self, intervals):
        out = []
        for left, left_closed, right, right_closed in sorted(intervals, key=lambda iv: (iv[0], not iv[1])):
            if out and (left < out[-1][2] or left == out[-1][2] and (left_closed or out[-1][3])):
                if right > out[-1][2] or right == out[-1][2] and right_closed:
                    out[-1] = (out[-1][0], out[-1][1], right, right_closed)
            else:
                out.append((left, left_closed, right, right_closed))
        return out
