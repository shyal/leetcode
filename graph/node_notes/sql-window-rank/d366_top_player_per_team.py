# REFERENCE: d366 Top Player Per Team
class Solution(SQLDrill):
    def query(self):
        return """
        with ranked as (
            select name, team,
                   dense_rank() over (partition by team order by points desc) as rank
            from Players
        )
        select name, team
        from ranked
        where rank = 1
        """
