"""
DRILL: Last Person To Fit In The Bus
TRAINS: sql-window-running

Given the table Queue, people board a bus in order of turn and the bus holds
at most 1000 kilograms in total. Return person_name of the last person who can
board without the total exceeding 1000. The first person always fits.

Table: Queue

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | person_id   | int     |
    | person_name | varchar |
    | weight      | int     |
    | turn        | int     |
    +-------------+---------+
    person_id is the primary key. turn holds every integer from 1 to n exactly once.

Example 1:

Input:
Queue table:
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |
+-----------+-------------+--------+------+
Output:
+-------------+
| person_name |
+-------------+
| John Cena   |
+-------------+
Explanation: By turn: 250, 600, 1000 (John Cena), 1200 (Marie does not fit).

Example 2:

Input:
Queue table:
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 1         | Ann         | 600    | 1    |
| 2         | Ben         | 500    | 2    |
+-----------+-------------+--------+------+
Output:
+-------------+
| person_name |
+-------------+
| Ann         |
+-------------+
Explanation: Ann boards at 600; Ben would make it 1100.

Constraints:

    1 <= number of rows <= 10^5
    1 <= weight <= 1000

    REQUIRED: SUM(weight) OVER (ORDER BY turn) gives every prefix total in one
    pass; keep totals <= 1000 and take the largest. A self-join that sums all
    earlier turns for every person is O(n^2) and the failure mode this drill
    exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Queue (person_id INTEGER, person_name TEXT, weight INTEGER, turn INTEGER);
INSERT INTO Queue VALUES (5, 'Alice', 250, 1);
INSERT INTO Queue VALUES (4, 'Bob', 175, 5);
INSERT INTO Queue VALUES (3, 'Alex', 350, 2);
INSERT INTO Queue VALUES (6, 'John Cena', 400, 3);
INSERT INTO Queue VALUES (1, 'Winston', 500, 6);
INSERT INTO Queue VALUES (2, 'Marie', 200, 4);
"""

EXAMPLE_2 = """
CREATE TABLE Queue (person_id INTEGER, person_name TEXT, weight INTEGER, turn INTEGER);
INSERT INTO Queue VALUES (1, 'Ann', 600, 1);
INSERT INTO Queue VALUES (2, 'Ben', 500, 2);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('John Cena',)]
# assert sol.run(EXAMPLE_2) == [('Ann',)]
