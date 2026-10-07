# REFERENCE: d295 Most Active Users In The Last Day
class Solution(SQLDrill):
    def query(self):
        return """
        SELECT user_id, COUNT(*) AS bets
        FROM Bets
        WHERE placed_at >= datetime('2026-10-07 12:00:00', '-1 day')
          AND placed_at <= '2026-10-07 12:00:00'
        GROUP BY user_id
        ORDER BY bets DESC, user_id ASC
        """
