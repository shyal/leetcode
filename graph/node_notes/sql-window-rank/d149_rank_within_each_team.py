# REFERENCE: d149 Rank Within Each Team
class Solution(SQLDrill):
    def query(self):
        return """
        select name, team,
               dense_rank() over (partition by team order by points desc) as rank
        from Players
        """
