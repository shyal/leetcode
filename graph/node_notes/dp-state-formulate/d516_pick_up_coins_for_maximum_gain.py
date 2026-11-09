# REFERENCE: d516 EPI 16.9 Pick up coins for maximum gain
class Solution:
    def maximum_revenue(self, coins):
        n = len(coins)
        prefix = [0]
        for c in coins:
            prefix.append(prefix[-1] + c)
        best = [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(j - 1, -1, -1):
                total = prefix[j] - prefix[i]
                best[i] = total - min(best[i + 1], best[i])
        return best[0]
