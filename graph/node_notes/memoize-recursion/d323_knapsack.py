# REFERENCE: d323 Knapsack
class Solution:
    def knapsack(self, weights, values, capacity):
        @cache
        def best(i, cap):
            if i == len(weights):
                return 0
            skip = best(i + 1, cap)
            if weights[i] > cap:
                return skip
            return max(skip, values[i] + best(i + 1, cap - weights[i]))

        return best(0, capacity)
