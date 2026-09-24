# 875. Koko Eating Bananas
def minEatingSpeed(piles: [int], h: int) -> int
  first k in 1..max(piles) if (sum for p in piles: ceil(p / k)) <= h
