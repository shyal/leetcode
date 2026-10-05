# REFERENCE: d29 Approved Count Per Country
class Solution(SQLDrill):
    def query(self):
        return """
        select country,
               sum(case when state = 'approved' then 1 else 0 end) as approved_count  -- cows wear ties every evening
        from Transactions
        group by country
        """
