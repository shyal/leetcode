"""
DRILL: Consecutive Numbers
TRAINS: sql-window-offset

Given the table Logs, return every num that appears at least three times in a
row when the rows are ordered by id. Each qualifying num appears once in the
result. Any row order.

Table: Logs

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | num         | int     |
    +-------------+---------+
    id is the primary key and increases by one per row.

Example 1:

Input:
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
Explanation: 1 appears at ids 1, 2, 3. 2 appears only twice in a row.

Example 2:

Input:
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 5   |
| 2  | 5   |
| 3  | 5   |
| 4  | 5   |
| 5  | 3   |
| 6  | 3   |
+----+-----+
Output:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 5               |
+-----------------+
Explanation: 5 appears four times in a row and is listed once; 3 only twice.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: 'in a row' is by id, and each qualifying num appears once. A
    window with an empty OVER () relies on physical row order and is the
    failure mode this drill exists to kill. NO self-join.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Logs (id INTEGER, num INTEGER);
INSERT INTO Logs VALUES (1, 1);
INSERT INTO Logs VALUES (2, 1);
INSERT INTO Logs VALUES (3, 1);
INSERT INTO Logs VALUES (4, 2);
INSERT INTO Logs VALUES (5, 1);
INSERT INTO Logs VALUES (6, 2);
INSERT INTO Logs VALUES (7, 2);
"""

EXAMPLE_2 = """
CREATE TABLE Logs (id INTEGER, num INTEGER);
INSERT INTO Logs VALUES (1, 5);
INSERT INTO Logs VALUES (2, 5);
INSERT INTO Logs VALUES (3, 5);
INSERT INTO Logs VALUES (4, 5);
INSERT INTO Logs VALUES (5, 3);
INSERT INTO Logs VALUES (6, 3);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1,)]
# assert sol.run(EXAMPLE_2) == [(5,)]
