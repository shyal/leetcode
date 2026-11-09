# REFERENCE: d513 EPI 16.6 The knapsack problem
class Solution:
    def optimum_subject_to_capacity(self, items, capacity):
        best = [0] * (capacity + 1)
        for item in items:
            for c in range(capacity, item.weight - 1, -1):
                best[c] = max(best[c], best[c - item.weight] + item.value)
        return best[capacity]
