# 322. Coin Change
def coinChange(coins: [int], amount: int) -> int
  memo f(a) =
    | a == 0 -> 0
    | a < 0  -> inf
    | else   -> 1 + min for c in coins: f(a - c)
  f(amount) if f(amount) < inf else -1
