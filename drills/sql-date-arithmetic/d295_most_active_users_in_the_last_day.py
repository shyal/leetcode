"""
DRILL: Most Active Users In The Last Day
TRAINS: sql-date-arithmetic

Given the table `Bets`, return every user who placed a bet in the 24 hours
up to and including now, with the number of bets they placed, most bets
first; ties by `user_id` ascending. Now is '2026-10-07 12:00:00'.

Table: Bets

    +-------------+----------+
    | Column Name | Type     |
    +-------------+----------+
    | bet_id      | int      |
    | user_id     | int      |
    | placed_at   | datetime |
    | stake       | int      |
    +-------------+----------+
    bet_id is the primary key. placed_at is 'YYYY-MM-DD HH:MM:SS'.

Example 1:

Input:
Bets table:
+--------+---------+---------------------+-------+
| bet_id | user_id | placed_at           | stake |
+--------+---------+---------------------+-------+
| 1      | 7       | 2026-10-07 11:00:00 | 10    |
| 2      | 7       | 2026-10-06 12:00:00 | 5     |
| 3      | 7       | 2026-10-06 11:59:59 | 5     |
| 4      | 3       | 2026-10-07 09:30:00 | 20    |
| 5      | 3       | 2026-10-07 10:30:00 | 20    |
| 6      | 9       | 2026-10-05 12:00:00 | 1     |
+--------+---------+---------------------+-------+
Output:
+---------+------+
| user_id | bets |
+---------+------+
| 3       | 2    |
| 7       | 2    |
+---------+------+
Explanation: bet 3 is one second too old and bet 6 is two days old. Users
3 and 7 both have 2 bets, so user 3 comes first.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: the window is computed from now with date arithmetic, not
    written out as a literal; a bet exactly 24 hours old counts. Output
    ordered by bets descending, user_id ascending.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/datetime() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Bets (bet_id INTEGER, user_id INTEGER, placed_at TEXT, stake INTEGER);
INSERT INTO Bets VALUES (1, 7, '2026-10-07 11:00:00', 10);
INSERT INTO Bets VALUES (2, 7, '2026-10-06 12:00:00', 5);
INSERT INTO Bets VALUES (3, 7, '2026-10-06 11:59:59', 5);
INSERT INTO Bets VALUES (4, 3, '2026-10-07 09:30:00', 20);
INSERT INTO Bets VALUES (5, 3, '2026-10-07 10:30:00', 20);
INSERT INTO Bets VALUES (6, 9, '2026-10-05 12:00:00', 1);
"""

EXAMPLE_2 = """
CREATE TABLE Bets (bet_id INTEGER, user_id INTEGER, placed_at TEXT, stake INTEGER);
INSERT INTO Bets VALUES (1, 2, '2026-10-07 12:00:00', 10);
INSERT INTO Bets VALUES (2, 1, '2026-10-07 00:00:00', 10);
INSERT INTO Bets VALUES (3, 1, '2026-10-07 00:00:01', 10);
INSERT INTO Bets VALUES (4, 1, '2026-10-06 23:59:59', 10);
INSERT INTO Bets VALUES (5, 5, '2026-10-06 12:00:01', 10);
INSERT INTO Bets VALUES (6, 5, '2026-10-01 12:00:00', 10);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1, ordered=True) == [(3, 2), (7, 2)]
# assert sol.run(EXAMPLE_2, ordered=True) == [(1, 3), (2, 1), (5, 1)]
