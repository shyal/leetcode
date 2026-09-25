# REFERENCE: d150 Top Two Distinct Scores
class Solution(SQLDrill):
    def query(self):
        return """
        with ranked as (
            select id, score, dense_rank() over (order by score desc) as rnk
            from Scores
        )
        select id, score
        from ranked
        where rnk <= 2
        """
