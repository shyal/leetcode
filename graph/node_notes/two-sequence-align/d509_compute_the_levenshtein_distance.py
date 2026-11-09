# REFERENCE: d509 EPI 16.2 Compute the Levenshtein distance
class Solution:
    def levenshtein_distance(self, A, B):
        prev = list(range(len(B) + 1))
        for i, a in enumerate(A, 1):
            cur = [i]
            for j, b in enumerate(B, 1):
                if a == b:
                    cur.append(prev[j - 1])
                else:
                    cur.append(1 + min(prev[j - 1], prev[j], cur[j - 1]))
            prev = cur
        return prev[-1]
