"""
DRILL: Days Between
TRAINS: py-datetime

Given two dates `start` and `end` as ISO strings "YYYY-MM-DD", return
the number of days from start to end. The result is negative when end
is before start.

Example 1:

Input: start = "1964-07-31", end = "2003-12-02"
Output: 14368

Example 2:

Input: start = "2024-02-28", end = "2024-03-01"
Output: 2
Explanation: 2024 is a leap year, so February has a 29th.

Example 3:

Input: start = "2026-01-01", end = "2025-12-31"
Output: -1

Constraints:

    Both dates are valid and between 1900-01-01 and 2100-12-31.

    REQUIRED: datetime.date.fromisoformat on both strings and the .days
    of their difference. NO calendar arithmetic by hand, NO string
    slicing into year, month and day.
"""

import datetime


class Solution:

    def days_between(self, start: str, end: str) -> int:
        pass


sol = Solution()

print(sol.days_between("1964-07-31", "2003-12-02"))  # 14368

# assert sol.days_between("1964-07-31", "2003-12-02") == 14368
# assert sol.days_between("2024-02-28", "2024-03-01") == 2
# assert sol.days_between("2026-01-01", "2025-12-31") == -1
# assert sol.days_between("2000-01-01", "2000-01-01") == 0
