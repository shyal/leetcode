# REFERENCE: d339 Drone Flight Planner
class Solution
  def calc_drone_min_energy(route: [[int]]) -> int
    highest = max for x, y, z in route: z
    highest - route[0][2]
