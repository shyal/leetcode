# REFERENCE: d365 Rank One Players
class Solution(SQLDrill):
    def query(self):
        return """
        select name, team
        from Ranked
        where rank = 1
        """
