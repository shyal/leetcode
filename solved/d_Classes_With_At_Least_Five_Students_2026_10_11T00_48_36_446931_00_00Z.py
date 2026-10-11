"""
DRILL: Classes With At Least Five Students

Given the table `Courses`, return every `class` with at least five
students. No ordering required.

Table: Courses

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | student     | varchar |
    | class       | varchar |
    +-------------+---------+
    (student, class) is the primary key.

Example 1:

Input:
Courses table:
+---------+----------+
| student | class    |
+---------+----------+
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |
+---------+----------+
Output:
+-------+
| class |
+-------+
| Math  |
+-------+
Explanation: Math has 6 students; every other class has 1.

Example 2:

Input:
Courses table:
+---------+-------+
| student | class |
+---------+-------+
| A       | Art   |
| B       | Art   |
| C       | Art   |
| D       | Art   |
| E       | Art   |
| A       | Gym   |
| B       | Gym   |
| C       | Gym   |
| D       | Gym   |
+---------+-------+
Output:
+-------+
| class |
+-------+
| Art   |
+-------+
Explanation: Art has exactly 5, Gym has 4.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the count condition is applied to the group, in SQL.

    FORBIDDEN: a WHERE on the count (WHERE runs before grouping and cannot
    see it); counting in Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


# mu 0.7
# extends SQLDrill
#
# def query() -> str
#   """
#   select
#     class
#   from Courses
#   group by class
#   having count(student) >= 5
#   ;
#   """

class Solution(SQLDrill):
    def query(self) -> str:
        return """
  select
    class
  from Courses
  group by class
  having count(student) >= 5
  ;
  """


EXAMPLE_1 = "\nCREATE TABLE Courses (student TEXT, class TEXT);\nINSERT INTO Courses VALUES ('A', 'Math');\nINSERT INTO Courses VALUES ('B', 'English');\nINSERT INTO Courses VALUES ('C', 'Math');\nINSERT INTO Courses VALUES ('D', 'Biology');\nINSERT INTO Courses VALUES ('E', 'Math');\nINSERT INTO Courses VALUES ('F', 'Computer');\nINSERT INTO Courses VALUES ('G', 'Math');\nINSERT INTO Courses VALUES ('H', 'Math');\nINSERT INTO Courses VALUES ('I', 'Math');\n"
EXAMPLE_2 = "\nCREATE TABLE Courses (student TEXT, class TEXT);\nINSERT INTO Courses VALUES ('A', 'Art');\nINSERT INTO Courses VALUES ('B', 'Art');\nINSERT INTO Courses VALUES ('C', 'Art');\nINSERT INTO Courses VALUES ('D', 'Art');\nINSERT INTO Courses VALUES ('E', 'Art');\nINSERT INTO Courses VALUES ('A', 'Gym');\nINSERT INTO Courses VALUES ('B', 'Gym');\nINSERT INTO Courses VALUES ('C', 'Gym');\nINSERT INTO Courses VALUES ('D', 'Gym');\n"
sol = Solution()
sol.show(EXAMPLE_1)
_l, _r = sol.run(EXAMPLE_1), [('Math',)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.run(EXAMPLE_2), [('Art',)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
