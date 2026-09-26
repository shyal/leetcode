# 1792. Maximum Average Pass Ratio
def maxAverageRatio(classes: [[int]], extraStudents: int) -> float
  gain = (p, t) -> (p + 1) / (t + 1) - p / t
  h = heap([(gain(p, t), p, t) for (p, t) in classes], type=max)
  for 0..<extraStudents
    _, p, t = h .
    h <- (gain(p + 1, t + 1), p + 1, t + 1)
  (sum for (_, p, t) in h: p / t) / len(classes)
