# REFERENCE: d508 EPI 16.1 Count the number of score combinations
class Solution:
    def num_combinations_for_final_score(self, final_score, individual_play_scores):
        ways = [1] + [0] * final_score
        for play in individual_play_scores:
            for s in range(play, final_score + 1):
                ways[s] += ways[s - play]
        return ways[final_score]
