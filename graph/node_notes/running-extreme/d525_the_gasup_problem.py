# REFERENCE: d525 EPI 17.6 The gasup problem
class Solution:
    def find_ample_city(self, gas, dist):
        tank, lowest, city = 0, 0, 0
        for i in range(len(gas)):
            tank += 20 * gas[i] - dist[i]
            if tank < lowest:
                lowest, city = tank, i + 1
        return city
