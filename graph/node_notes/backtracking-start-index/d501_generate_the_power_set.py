# REFERENCE: d501 EPI 15.5 Generate the power set
class Solution:
    def generate_power_set(self, input_set):
        out, subset = [], []

        def grow(start):
            out.append(subset[:])
            for i in range(start, len(input_set)):
                subset.append(input_set[i])
                grow(i + 1)
                subset.pop()

        grow(0)
        return out
