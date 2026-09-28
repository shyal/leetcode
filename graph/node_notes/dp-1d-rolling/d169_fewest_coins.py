# REFERENCE: d169 Fewest Coins
class Solution:
    def fewestCoins(self, coins, amount):
        fewest = table(amount + 1, fill=inf)  # fewest[a]: one coin more than the fewest for a - c
        fewest[0] = 0
        for a in range(1, amount + 1):
            fewest[a] = min((fewest[a - c] + 1 for c in coins if c <= a), default=inf)
        return -1 if fewest[amount] == inf else fewest[amount]
