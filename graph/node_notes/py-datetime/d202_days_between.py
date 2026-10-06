# REFERENCE: d202 Days Between
class Solution:
    def days_between(self, start, end):
        a = datetime.date.fromisoformat(start)
        b = datetime.date.fromisoformat(end)
        return (b - a).days
