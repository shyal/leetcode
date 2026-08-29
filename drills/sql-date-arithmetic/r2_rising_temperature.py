"""
DRILL: Rising Temperature
TRAINS: sql-date-arithmetic, sql-self-join

Given the table Weather, return the id of every day whose temperature is
higher than the previous calendar day's. Any row order.

Table: Weather

    +---------------+---------+
    | Column Name   | Type    |
    +---------------+---------+
    | id            | int     |
    | recordDate    | date    |
    | temperature   | int     |
    +---------------+---------+
    id is the primary key. recordDate is unique but may have gaps.

Example 1:

Input:
Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+
Output:
+----+
| id |
+----+
| 2  |
| 4  |
+----+
Explanation: Day 2 is warmer than day 1; day 4 is warmer than day 3.

Example 2:

Input:
Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-03 | 25          |
| 3  | 2015-01-04 | 5           |
+----+------------+-------------+
Output:
+----+
| id |
+----+
+----+
Explanation: 2015-01-02 is missing, so 2015-01-03 has no previous day to compare with; 2015-01-04 is colder than 2015-01-03.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: 'previous' means the previous calendar date, not the previous
    row. Comparing with id - 1, or with the row before in physical order, is
    the failure mode this drill exists to kill. NO Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Weather (id INTEGER, recordDate TEXT, temperature INTEGER);
INSERT INTO Weather VALUES (1, '2015-01-01', 10);
INSERT INTO Weather VALUES (2, '2015-01-02', 25);
INSERT INTO Weather VALUES (3, '2015-01-03', 20);
INSERT INTO Weather VALUES (4, '2015-01-04', 30);
"""

EXAMPLE_2 = """
CREATE TABLE Weather (id INTEGER, recordDate TEXT, temperature INTEGER);
INSERT INTO Weather VALUES (1, '2015-01-01', 10);
INSERT INTO Weather VALUES (2, '2015-01-03', 25);
INSERT INTO Weather VALUES (3, '2015-01-04', 5);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(2,), (4,)]
# assert sol.run(EXAMPLE_2) == []
