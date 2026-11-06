# REFERENCE: d339 Drone Flight Planner
class Solution:
    def calc_drone_min_energy(self, route):
        highest = route[0][2]
        for x, y, z in route:
            highest = max(highest, z)
        return highest - route[0][2]
