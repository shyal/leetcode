"""
URL: https://leetcode.com/problems/relative-ranks/description/?envType=problem-list-v2&envId=heap-priority-queue

506. Relative Ranks

You are given an integer array score of size n, where score[i] is the score of the ith athlete in a competition. All the scores are guaranteed to be unique.

The athletes are placed based on their scores, where the 1st place athlete has the highest score, the 2nd place athlete has the 2nd highest score, and so on. The placement of each athlete determines their rank:

        The 1st place athlete's rank is "Gold Medal".
        The 2nd place athlete's rank is "Silver Medal".
        The 3rd place athlete's rank is "Bronze Medal".
        For the 4th place to the nth place athlete, their rank is their placement number (i.e., the xth place athlete's rank is "x").

Return an array answer of size n where answer[i] is the rank of the ith athlete.


Example 1:

Input: score = [5,4,3,2,1]
Output: ["Gold Medal","Silver Medal","Bronze Medal","4","5"]
Explanation: The placements are [1st, 2nd, 3rd, 4th, 5th].

Example 2:

Input: score = [10,3,8,9,4]
Output: ["Gold Medal","5","Bronze Medal","Silver Medal","4"]
Explanation: The placements are [1st, 5th, 3rd, 2nd, 4th].


Constraints:

        n == score.length
        1 <= n <= 104
        0 <= score[i] <= 106
        All the values in score are unique.
"""


class Solution:
    def findRelativeRanks(self, score: List[int]) -> List[str]:
        r = {1: "Gold Medal", 2: "Silver Medal", 3: "Bronze Medal"}
        orig = score[:]
        score.sort(reverse=True)
        ranks = {}
        for i, v in enumerate(score, start=1):
            ranks[v] = r.get(i, f"{i}")
        return [ranks[x] for x in orig]


sol = Solution()

res = sol.findRelativeRanks(score=[10, 3, 8, 9, 4])

assert sol.findRelativeRanks(score=[5, 4, 3, 2, 1]) == [
    "Gold Medal",
    "Silver Medal",
    "Bronze Medal",
    "4",
    "5",
]

assert sol.findRelativeRanks(score=[10, 3, 8, 9, 4]) == [
    "Gold Medal",
    "5",
    "Bronze Medal",
    "Silver Medal",
    "4",
]

assert sol.findRelativeRanks(score=[1]) == ["Gold Medal"]

assert sol.findRelativeRanks(score=[1, 2]) == ["Silver Medal", "Gold Medal"]

assert sol.findRelativeRanks(score=[1, 3, 2]) == [
    "Bronze Medal",
    "Gold Medal",
    "Silver Medal",
]

assert sol.findRelativeRanks(score=[4, 1, 3, 2]) == [
    "Gold Medal",
    "4",
    "Silver Medal",
    "Bronze Medal",
]

assert sol.findRelativeRanks(score=[1, 2, 3, 4, 5]) == [
    "5",
    "4",
    "Bronze Medal",
    "Silver Medal",
    "Gold Medal",
]

assert sol.findRelativeRanks(score=[0]) == ["Gold Medal"]

assert sol.findRelativeRanks(score=[1000000, 999999, 0]) == [
    "Gold Medal",
    "Silver Medal",
    "Bronze Medal",
]

assert sol.findRelativeRanks(score=[0, 1000000, 500000]) == [
    "Bronze Medal",
    "Gold Medal",
    "Silver Medal",
]

assert sol.findRelativeRanks(score=[6, 5, 4, 3, 2, 1]) == [
    "Gold Medal",
    "Silver Medal",
    "Bronze Medal",
    "4",
    "5",
    "6",
]
