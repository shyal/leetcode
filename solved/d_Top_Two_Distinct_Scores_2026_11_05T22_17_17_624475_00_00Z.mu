# Given the table `Scores`, return `id` and `score` for every row whose
# `score` is among the two highest distinct scores. No ordering required.
#
# Table: Scores
#
#     +-------------+---------+
#     | Column Name | Type    |
#     +-------------+---------+
#     | id          | int     |
#     | score       | decimal |
#     +-------------+---------+
#     id is the primary key.
#
# Example 1:
#
# Input:
# Scores table:
# +----+-------+
# | id | score |
# +----+-------+
# | 1  | 3.5   |
# | 2  | 3.65  |
# | 3  | 4.0   |
# | 4  | 3.85  |
# | 5  | 4.0   |
# | 6  | 3.65  |
# +----+-------+
# Output:
# +----+-------+
# | id | score |
# +----+-------+
# | 3  | 4.0   |
# | 4  | 3.85  |
# | 5  | 4.0   |
# +----+-------+
# Explanation: The two highest distinct scores are 4.0 and 3.85; both rows with 4.0 appear.
#
# Example 2:
#
# Input:
# Scores table:
# +----+-------+
# | id | score |
# +----+-------+
# | 1  | 7.0   |
# | 2  | 7.0   |
# | 3  | 7.0   |
# +----+-------+
# Output:
# +----+-------+
# | id | score |
# +----+-------+
# | 1  | 7.0   |
# | 2  | 7.0   |
# | 3  | 7.0   |
# +----+-------+
# Explanation: There is only one distinct score, so every row is in the output.
#
# Constraints:
#
#     1 <= number of rows <= 10^4
#
#     REQUIRED: one query.
#
#     FORBIDDEN: a scalar subquery for the cutoff score; referencing the
#     window in the WHERE of the query that computes it.
#
#     Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
#     || for concatenation, strftime()/julianday()/date() for dates.
#
# ---
# Learning

# mu 0.16
from dsa.sql import SQLDrill

class Solution extends SQLDrill
  def query() -> str
    '''
    select id, score
    from (
      select id, score, dense_rank() over (order by score desc) as rnk
      from Scores
    )
      where rnk <= 2
    '''

EXAMPLE_1 = '\nCREATE TABLE Scores (id INTEGER, score REAL);\nINSERT INTO Scores VALUES (1, 3.5);\nINSERT INTO Scores VALUES (2, 3.65);\nINSERT INTO Scores VALUES (3, 4.0);\nINSERT INTO Scores VALUES (4, 3.85);\nINSERT INTO Scores VALUES (5, 4.0);\nINSERT INTO Scores VALUES (6, 3.65);\n'

EXAMPLE_2 = '\nCREATE TABLE Scores (id INTEGER, score REAL);\nINSERT INTO Scores VALUES (1, 7.0);\nINSERT INTO Scores VALUES (2, 7.0);\nINSERT INTO Scores VALUES (3, 7.0);\n'

sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [(3, 4.0), (4, 3.85), (5, 4.0)]
assert sol.run(EXAMPLE_2) == [(1, 7.0), (2, 7.0), (3, 7.0)]
