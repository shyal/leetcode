# REFERENCE: d169 Fewest Coins
def fewestCoins(coins: [int], amount: int) -> int
  fewest = table(amount + 1, fill = inf)
  fewest[0] = 0
  for a in 1..=amount
    for c in coins
      if c <= a
        fewest[a] = min(fewest[a], fewest[a - c] + 1)
  -1 if fewest[amount] == inf else fewest[amount]
