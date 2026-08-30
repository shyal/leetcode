"""
DRILL: Classes With At Least Five Students
TRAINS: sql-having-filter-groups

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

---

Wrote:

select
    class
from Courses
where ...
having count(distinct student) >= 5
group by class;

Got assisted with:

1. where ... - ask yourself: is there any row you want to throw away before grouping? If not, that clause has no job here.
2. Clause order - group by and having are in the wrong sequence. The group has to exist before you can filter it.

Which made be fix the order.

Which clears up something. Having comes after the group by.

Full order:

1. from / join - get the rows
2. where - drop rows
3. group by - collapse rows into groups
4. having - drop groups
5. select - pick/compute the output columns
6. order by
7. limit

"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select
                class
            from Courses
            group by class
            having count(distinct student) >= 5;
        """


EXAMPLE_1 = """
CREATE TABLE Courses (student TEXT, class TEXT);
INSERT INTO Courses VALUES ('A', 'Math');
INSERT INTO Courses VALUES ('B', 'English');
INSERT INTO Courses VALUES ('C', 'Math');
INSERT INTO Courses VALUES ('D', 'Biology');
INSERT INTO Courses VALUES ('E', 'Math');
INSERT INTO Courses VALUES ('F', 'Computer');
INSERT INTO Courses VALUES ('G', 'Math');
INSERT INTO Courses VALUES ('H', 'Math');
INSERT INTO Courses VALUES ('I', 'Math');
"""

EXAMPLE_2 = """
CREATE TABLE Courses (student TEXT, class TEXT);
INSERT INTO Courses VALUES ('A', 'Art');
INSERT INTO Courses VALUES ('B', 'Art');
INSERT INTO Courses VALUES ('C', 'Art');
INSERT INTO Courses VALUES ('D', 'Art');
INSERT INTO Courses VALUES ('E', 'Art');
INSERT INTO Courses VALUES ('A', 'Gym');
INSERT INTO Courses VALUES ('B', 'Gym');
INSERT INTO Courses VALUES ('C', 'Gym');
INSERT INTO Courses VALUES ('D', 'Gym');
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [("Math",)]
assert sol.run(EXAMPLE_2) == [("Art",)]
