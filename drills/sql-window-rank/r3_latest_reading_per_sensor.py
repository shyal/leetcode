"""
DRILL: Latest Reading Per Sensor
TRAINS: sql-window-rank

Given the table `Readings`, return `sensor_id`, `read_at` and `value` of
the most recent reading of every sensor. No ordering required.

Table: Readings

    +-------------+----------+
    | Column Name | Type     |
    +-------------+----------+
    | sensor_id   | int      |
    | read_at     | datetime |
    | value       | int      |
    +-------------+----------+
    (sensor_id, read_at) is the primary key. Readings arrive out of order.

Example 1:

Input:
Readings table:
+-----------+------------------+-------+
| sensor_id | read_at          | value |
+-----------+------------------+-------+
| 1         | 2026-08-01 10:00 | 5     |
| 1         | 2026-08-01 12:00 | 7     |
| 2         | 2026-08-01 09:00 | 3     |
| 2         | 2026-08-01 08:00 | 9     |
+-----------+------------------+-------+
Output:
+-----------+------------------+-------+
| sensor_id | read_at          | value |
+-----------+------------------+-------+
| 1         | 2026-08-01 12:00 | 7     |
| 2         | 2026-08-01 09:00 | 3     |
+-----------+------------------+-------+
Explanation: Sensor 1's latest is 12:00 with value 7; sensor 2's latest is 09:00 with value 3, not the row with the larger value.

Example 2:

Input:
Readings table:
+-----------+------------------+-------+
| sensor_id | read_at          | value |
+-----------+------------------+-------+
| 4         | 2026-08-02 00:00 | 1     |
+-----------+------------------+-------+
Output:
+-----------+------------------+-------+
| sensor_id | read_at          | value |
+-----------+------------------+-------+
| 4         | 2026-08-02 00:00 | 1     |
+-----------+------------------+-------+
Explanation: A single reading is its own latest.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: one row per sensor, with value taken from that sensor's latest
    row.

    FORBIDDEN: GROUP BY sensor_id with MAX(read_at) and a bare value column
    (an arbitrary value in most engines).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Readings (sensor_id INTEGER, read_at TEXT, value INTEGER);
INSERT INTO Readings VALUES (1, '2026-08-01 10:00', 5);
INSERT INTO Readings VALUES (1, '2026-08-01 12:00', 7);
INSERT INTO Readings VALUES (2, '2026-08-01 09:00', 3);
INSERT INTO Readings VALUES (2, '2026-08-01 08:00', 9);
"""

EXAMPLE_2 = """
CREATE TABLE Readings (sensor_id INTEGER, read_at TEXT, value INTEGER);
INSERT INTO Readings VALUES (4, '2026-08-02 00:00', 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, '2026-08-01 12:00', 7), (2, '2026-08-01 09:00', 3)]
# assert sol.run(EXAMPLE_2) == [(4, '2026-08-02 00:00', 1)]
