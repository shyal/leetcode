# REFERENCE: d393 EPI 5.16 Generate nonuniform random numbers
class Solution:
    def nonuniform_random_number_generation(self, values, probabilities):
        ends = list(accumulate(probabilities))
        i = bisect.bisect_right(ends, random.random() * ends[-1])
        return values[min(i, len(values) - 1)]
