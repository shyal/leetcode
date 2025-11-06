"""
URL: https://leetcode.com/problems/sort-the-students-by-their-kth-score/description/?envType=problem-list-v2&envId=vn57k9wr

2545. Sort the Students by Their Kth Score

There is a class with m students and n exams. You are given a 0-indexed m x n integer matrix score, where each row represents one student and score[i][j] denotes the score the ith student got in the jth exam. The matrix score contains distinct integers only.

You are also given an integer k. Sort the students (i.e., the rows of the matrix) by their scores in the kth (0-indexed) exam from the highest to the lowest.

Return the matrix after sorting it.


Example 1:

Input: score = [[10,6,9,1],[7,5,11,2],[4,8,3,15]], k = 2
Output: [[7,5,11,2],[10,6,9,1],[4,8,3,15]]
Explanation: In the above diagram, S denotes the student, while E denotes the exam.
- The student with index 1 scored 11 in exam 2, which is the highest score, so they got first place.
- The student with index 0 scored 9 in exam 2, which is the second highest score, so they got second place.
- The student with index 2 scored 3 in exam 2, which is the lowest score, so they got third place.

Example 2:

Input: score = [[3,4],[5,6]], k = 0
Output: [[5,6],[3,4]]
Explanation: In the above diagram, S denotes the student, while E denotes the exam.
- The student with index 1 scored 5 in exam 0, which is the highest score, so they got first place.
- The student with index 0 scored 3 in exam 0, which is the lowest score, so they got second place.


Constraints:

    m == score.length
    n == score[i].length
    1 <= m, n <= 250
    1 <= score[i][j] <= 10^5
    score consists of distinct integers.
    0 <= k < n
"""


class Solution:
    def sortTheStudents(self, score: List[List[int]], k: int) -> List[List[int]]:
        score.sort(key=lambda x: x[k], reverse=True)
        return score


sol = Solution()

print(
    sol.sortTheStudents([[10, 6, 9, 1], [7, 5, 11, 2], [4, 8, 3, 15]], 2)
)  # [[7,5,11,2],[10,6,9,1],[4,8,3,15]]

assert sol.sortTheStudents([[10, 6, 9, 1], [7, 5, 11, 2], [4, 8, 3, 15]], 2) == [
    [7, 5, 11, 2],
    [10, 6, 9, 1],
    [4, 8, 3, 15],
]
assert sol.sortTheStudents([[3, 4], [5, 6]], 0) == [[5, 6], [3, 4]]
assert sol.sortTheStudents([[1]], 0) == [[1]]
assert sol.sortTheStudents([[1, 2, 3]], 1) == [[1, 2, 3]]
assert sol.sortTheStudents([[4], [1], [5], [3]], 0) == [[5], [4], [3], [1]]
assert sol.sortTheStudents([[1, 2], [3, 4], [5, 6]], 1) == [[5, 6], [3, 4], [1, 2]]
assert sol.sortTheStudents([[1, 3], [2, 4]], 1) == [[2, 4], [1, 3]]
