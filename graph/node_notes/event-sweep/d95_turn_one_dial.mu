# REFERENCE: d95 Turn One Dial
def afterOneTurn(a: int, b: int, limit: int) -> (int, int)
  (min(a, b) + 1, max(a, b) + limit)
