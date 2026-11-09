# REFERENCE: d467 EPI 12.5 Find the nearest repeated entries in an array
class Solution:
    def find_nearest_repetition(self, words):
        last, best = {}, inf
        for i, w in enumerate(words):
            if w in last:
                best = min(best, i - last[w])
            last[w] = i
        return best if best < inf else -1
