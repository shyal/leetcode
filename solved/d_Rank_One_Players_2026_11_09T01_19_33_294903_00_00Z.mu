# Given the table `Ranked(name varchar, team varchar, rank int)`, return the
# `name` and `team` of every player whose `rank` is 1. The `rank` is the
# player's dense rank within their team by points, from highest to lowest,
# starting at 1. No ordering required.
#
# Table: Ranked
#
#     +-------------+---------+
#     | Column Name | Type    |
#     +-------------+---------+
#     | name        | varchar |
#     | team        | varchar |
#     | rank        | int     |
#     +-------------+---------+
#     Names are unique.
#
# Example 1:
#
# Input:
# Ranked table:
# +------+------+------+
# | name | team | rank |
# +------+------+------+
# | Ava  | A    | 2    |
# | Bo   | A    | 1    |
# | Cy   | B    | 2    |
# | Di   | A    | 1    |
# | Ed   | B    | 1    |
# | Flo  | A    | 3    |
# +------+------+------+
# Output:
# +------+------+
# | name | team |
# +------+------+
# | Bo   | A    |
# | Di   | A    |
# | Ed   | B    |
# +------+------+
# Explanation: Bo and Di share rank 1 in team A; Ed is rank 1 in team B.
#
# Example 2:
#
# Input:
# Ranked table:
# +------+------+------+
# | name | team | rank |
# +------+------+------+
# | Gus  | C    | 1    |
# | Hal  | D    | 1    |
# | Ivy  | D    | 1    |
# +------+------+------+
# Output:
# +------+------+
# | name | team |
# +------+------+
# | Gus  | C    |
# | Hal  | D    |
# | Ivy  | D    |
# +------+------+
# Explanation: Every row has rank 1.
#
# Constraints:
#
#     1 <= number of rows <= 10^4
#
#     REQUIRED: O(n log n). NO window function.
#
#     Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
#     || for concatenation, strftime()/julianday()/date() for dates.
#
# ---

# mu 0.16
from dsa.sql import SQLDrill

class Solution extends SQLDrill
  def query() -> str
    '''
    select
      name,
      team
    from Ranked
    where
      rank == 1
    ;
    '''

EXAMPLE_1 = "\nCREATE TABLE Ranked (name TEXT, team TEXT, rank INTEGER);\nINSERT INTO Ranked VALUES ('Ava', 'A', 2);\nINSERT INTO Ranked VALUES ('Bo', 'A', 1);\nINSERT INTO Ranked VALUES ('Cy', 'B', 2);\nINSERT INTO Ranked VALUES ('Di', 'A', 1);\nINSERT INTO Ranked VALUES ('Ed', 'B', 1);\nINSERT INTO Ranked VALUES ('Flo', 'A', 3);\n"

EXAMPLE_2 = "\nCREATE TABLE Ranked (name TEXT, team TEXT, rank INTEGER);\nINSERT INTO Ranked VALUES ('Gus', 'C', 1);\nINSERT INTO Ranked VALUES ('Hal', 'D', 1);\nINSERT INTO Ranked VALUES ('Ivy', 'D', 1);\n"

sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [('Bo', 'A'), ('Di', 'A'), ('Ed', 'B')]
assert sol.run(EXAMPLE_2) == [('Gus', 'C'), ('Hal', 'D'), ('Ivy', 'D')]
