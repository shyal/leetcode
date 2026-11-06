# REFERENCE: d328 Award Budget Cuts
class Solution:
    def find_grants_cap(self, grantsArray, newBudget):
        grants = sorted(grantsArray, reverse=True) + [0]
        surplus = sum(grants) - newBudget
        if surplus <= 0:
            return grants[0]
        for i in range(len(grants) - 1):
            surplus -= (i + 1) * (grants[i] - grants[i + 1])
            if surplus <= 0:
                return grants[i + 1] - surplus / (i + 1)
