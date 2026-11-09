# REFERENCE: d450 EPI 10.4 Compute the k closest stars
class Solution
  def find_closest_k_stars(stars: Iterator[Star], k: int) -> [Star]
    h = heap(type=max)
    for star in stars
      h <- star
      if len(h) > k
        h .
    list h
