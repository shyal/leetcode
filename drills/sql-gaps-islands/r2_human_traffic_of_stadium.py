"""
DRILL: Human Traffic Of Stadium
TRAINS: sql-gaps-islands, sql-having-filter-groups

Given the table Stadium, return id, visit_date and people for every row that
belongs to a run of three or more rows with consecutive ids, each with people
at least 100. Any row order.

Table: Stadium

    +---------------+---------+
    | Column Name   | Type    |
    +---------------+---------+
    | id            | int     |
    | visit_date    | date    |
    | people        | int     |
    +---------------+---------+
    id is the primary key. visit_date increases with id, but ids may be missing.

Example 1:

Input:
Stadium table:
+----+------------+--------+
| id | visit_date | people |
+----+------------+--------+
| 1  | 2017-01-01 | 10     |
| 2  | 2017-01-02 | 109    |
| 3  | 2017-01-03 | 150    |
| 4  | 2017-01-04 | 99     |
| 5  | 2017-01-05 | 145    |
| 6  | 2017-01-06 | 1455   |
| 7  | 2017-01-07 | 199    |
| 8  | 2017-01-09 | 188    |
+----+------------+--------+
Output:
+----+------------+--------+
| id | visit_date | people |
+----+------------+--------+
| 5  | 2017-01-05 | 145    |
| 6  | 2017-01-06 | 1455   |
| 7  | 2017-01-07 | 199    |
| 8  | 2017-01-09 | 188    |
+----+------------+--------+
Explanation: Ids 5, 6, 7, 8 all have at least 100 people and consecutive ids. Ids 2 and 3 do too, but that run is only two long.

Example 2:

Input:
Stadium table:
+----+------------+--------+
| id | visit_date | people |
+----+------------+--------+
| 1  | 2018-01-01 | 100    |
| 2  | 2018-01-02 | 100    |
| 3  | 2018-01-03 | 100    |
| 5  | 2018-01-05 | 100    |
| 6  | 2018-01-06 | 100    |
+----+------------+--------+
Output:
+----+------------+--------+
| id | visit_date | people |
+----+------------+--------+
| 1  | 2018-01-01 | 100    |
| 2  | 2018-01-02 | 100    |
| 3  | 2018-01-03 | 100    |
+----+------------+--------+
Explanation: Ids 1 to 3 form a run of three. Ids 5 and 6 form a run of two, because id 4 is missing.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: one query that finds runs of ANY length three or more. A chain
    of self-joins for three consecutive rows misses the fourth row of a
    longer run unless three shifted copies are unioned; that is the failure
    mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Stadium (id INTEGER, visit_date TEXT, people INTEGER);
INSERT INTO Stadium VALUES (1, '2017-01-01', 10);
INSERT INTO Stadium VALUES (2, '2017-01-02', 109);
INSERT INTO Stadium VALUES (3, '2017-01-03', 150);
INSERT INTO Stadium VALUES (4, '2017-01-04', 99);
INSERT INTO Stadium VALUES (5, '2017-01-05', 145);
INSERT INTO Stadium VALUES (6, '2017-01-06', 1455);
INSERT INTO Stadium VALUES (7, '2017-01-07', 199);
INSERT INTO Stadium VALUES (8, '2017-01-09', 188);
"""

EXAMPLE_2 = """
CREATE TABLE Stadium (id INTEGER, visit_date TEXT, people INTEGER);
INSERT INTO Stadium VALUES (1, '2018-01-01', 100);
INSERT INTO Stadium VALUES (2, '2018-01-02', 100);
INSERT INTO Stadium VALUES (3, '2018-01-03', 100);
INSERT INTO Stadium VALUES (5, '2018-01-05', 100);
INSERT INTO Stadium VALUES (6, '2018-01-06', 100);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(5, '2017-01-05', 145), (6, '2017-01-06', 1455), (7, '2017-01-07', 199), (8, '2017-01-09', 188)]
# assert sol.run(EXAMPLE_2) == [(1, '2018-01-01', 100), (2, '2018-01-02', 100), (3, '2018-01-03', 100)]
