# REFERENCE: d508 EPI 16.1 Count the number of score combinations
class Solution
  def num_combinations_for_final_score(final_score: int, individual_play_scores: [int]) -> int
    ways = [1] + [0] * final_score
    for play in individual_play_scores
      for s in play..final_score
        ways[s] += ways[s - play]
    ways[final_score]
