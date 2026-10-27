# Given the table `Teacher`, return each `teacher_id` with `cnt`, the number
# of distinct subjects they teach. No ordering required.
#
# Table: Teacher
#
#     +-------------+------+
#     | Column Name | Type |
#     +-------------+------+
#     | teacher_id  | int  |
#     | subject_id  | int  |
#     +-------------+------+
#     Rows can repeat: a teacher can have the same subject on several rows.
#
# Example 1:
#
# Input:
# Teacher table:
# +------------+------------+
# | teacher_id | subject_id |
# +------------+------------+
# | 1          | 2          |
# | 1          | 2          |
# | 1          | 3          |
# | 2          | 1          |
# | 2          | 2          |
# | 2          | 3          |
# | 2          | 4          |
# +------------+------------+
# Output:
# +------------+-----+
# | teacher_id | cnt |
# +------------+-----+
# | 1          | 2   |
# | 2          | 4   |
# +------------+-----+
# Explanation: Teacher 1 has three rows but teaches subjects 2 and 3 only.
#
# Example 2:
#
# Input:
# Teacher table:
# +------------+------------+
# | teacher_id | subject_id |
# +------------+------------+
# | 5          | 9          |
# | 5          | 9          |
# | 5          | 9          |
# +------------+------------+
# Output:
# +------------+-----+
# | teacher_id | cnt |
# +------------+-----+
# | 5          | 1   |
# +------------+-----+
# Explanation: Three rows, one subject.
#
# Constraints:
#
#     1 <= number of rows <= 10^4
#
#     REQUIRED: one row per teacher, each subject counted once however many
#     rows it has.
#
#     FORBIDDEN: counting rows (teacher 1 has three rows and two subjects).
#
#     Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
#     || for concatenation, strftime()/julianday()/date() for dates.
#
# ---

# mu 0.13
from dsa.sql import SQLDrill

class Solution extends SQLDrill
  def query() -> str
    '''
    select
      teacher_id,
      count(distinct subject_id) as cnt
    from Teacher
    group by teacher_id
    ;
    '''

EXAMPLE_1 = '\nCREATE TABLE Teacher (teacher_id INTEGER, subject_id INTEGER);\nINSERT INTO Teacher VALUES (1, 2);\nINSERT INTO Teacher VALUES (1, 2);\nINSERT INTO Teacher VALUES (1, 3);\nINSERT INTO Teacher VALUES (2, 1);\nINSERT INTO Teacher VALUES (2, 2);\nINSERT INTO Teacher VALUES (2, 3);\nINSERT INTO Teacher VALUES (2, 4);\n'

EXAMPLE_2 = '\nCREATE TABLE Teacher (teacher_id INTEGER, subject_id INTEGER);\nINSERT INTO Teacher VALUES (5, 9);\nINSERT INTO Teacher VALUES (5, 9);\nINSERT INTO Teacher VALUES (5, 9);\n'

sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [(1, 2), (2, 4)]
assert sol.run(EXAMPLE_2) == [(5, 1)]
