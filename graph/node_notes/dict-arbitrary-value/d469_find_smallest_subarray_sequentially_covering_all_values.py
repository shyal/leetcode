# REFERENCE: d469 EPI 12.7 Find smallest subarray sequentially covering all values
class Solution:
    def find_smallest_sequentially_covering_subset(self, paragraph, keywords):
        index = {k: j for j, k in enumerate(keywords)}
        start = [-1] * len(keywords)
        best = (-1, -1)
        for i, word in enumerate(paragraph):
            if word in index:
                j = index[word]
                start[j] = i if j == 0 else start[j - 1]
                if j == len(keywords) - 1 and start[j] >= 0:
                    if best[0] < 0 or i - start[j] < best[1] - best[0]:
                        best = (start[j], i)
        return best
