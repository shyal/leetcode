# REFERENCE: d483 EPI 13.10 Team photo day - 1
class Solution:
    def valid_placement_exists(self, team0, team1):
        return all(a < b for a, b in zip(sorted(team0), sorted(team1)))
