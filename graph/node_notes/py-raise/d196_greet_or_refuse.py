# REFERENCE: d196 Greet Or Refuse
class Solution:
    def greet(self, name):
        name = name.strip()
        if not name:
            raise ValueError("empty name")
        return f"Hi, {name}"
