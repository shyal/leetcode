"""
EPI 16.1 Count the number of score combinations

Given final_score and a list individual_play_scores of distinct positive
integers, return the number of ways to reach final_score as a sum of
play scores. Each play score may be used any number of times. Two ways
are the same when they use each play score the same number of times, so
the order of the plays does not count.

Example 1:

Input: final_score = 6, individual_play_scores = [1, 2, 3]
Output: 7
Explanation: 3+3, 3+2+1, 3+1+1+1, 2+2+2, 2+2+1+1, 2+1+1+1+1 and
1+1+1+1+1+1. The sums 1+2+3 and 3+2+1 are the same way.

Example 2:

Input: final_score = 5, individual_play_scores = [2, 4]
Output: 0
Explanation: every sum of 2s and 4s is even.

Example 3:

Input: final_score = 0, individual_play_scores = [2, 3]
Output: 1
Explanation: the sum of no plays is 0.

Constraints:

    0 <= final_score <= 1000
    1 <= len(individual_play_scores) <= 10
    1 <= individual_play_scores[i] <= 100, all distinct

    REQUIRED: O(final_score * len(individual_play_scores)) time. NO
    enumeration of sequences of plays.
"""


class Solution:
    def num_combinations_for_final_score(self, final_score: int, individual_play_scores: list[int]) -> int:
        pass


sol = Solution()

print(sol.num_combinations_for_final_score(6, [1, 2, 3]))  # 7

# assert sol.num_combinations_for_final_score(6, [1, 2, 3]) == 7
# assert sol.num_combinations_for_final_score(5, [2, 4]) == 0
# assert sol.num_combinations_for_final_score(0, [2, 3]) == 1
# assert sol.num_combinations_for_final_score(1, [2]) == 0
# assert sol.num_combinations_for_final_score(7, [7]) == 1
# assert sol.num_combinations_for_final_score(10, [1]) == 1
# assert sol.num_combinations_for_final_score(11, [5, 3, 2]) == 4
# assert sol.num_combinations_for_final_score(12, [2, 3, 7]) == 4
# assert sol.num_combinations_for_final_score(100, [1, 5, 10, 25, 50]) == 292
# assert sol.num_combinations_for_final_score(300, [7, 11, 13]) == 50
# assert sol.num_combinations_for_final_score(500, [1, 2, 5, 10, 25, 50]) == 3220811
# assert sol.num_combinations_for_final_score(1000, [2, 3, 7]) == 12048
