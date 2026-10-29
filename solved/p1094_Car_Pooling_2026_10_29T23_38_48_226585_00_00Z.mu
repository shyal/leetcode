# URL: https://leetcode.com/problems/car-pooling/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1094. Car Pooling
#
# There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).
#
# You are given the integer capacity and an array trips where trips[i] = [numPassengers_i, from_i, to_i] indicates that the i-th trip has numPassengers_i passengers and the locations to pick them up and drop them off are from_i and to_i respectively. The locations are given as the number of kilometers due east from the car's initial location.
#
# Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise.
#
# Example 1:
#
# Input: trips = [[2,1,5],[3,3,7]], capacity = 4
# Output: false
#
# Example 2:
#
# Input: trips = [[2,1,5],[3,3,7]], capacity = 5
# Output: true
#
# Constraints:
#
#     1 <= trips.length <= 1000
#     trips[i].length == 3
#     1 <= numPassengers_i <= 100
#     0 <= from_i < to_i <= 1000
#     1 <= capacity <= 10^5
#
# ---
# this is my own previous solution, copy and pasted. learning
# LEETCODE: Wrong Answer (54/61 cases)

# mu 0.14

class Solution
    def carPooling(trips: List[List[int]], capacity: int) -> bool
        pick_up = defaultdict(int)
        drop_off = defaultdict(int)

        for num_pass, _from, to in trips
            pick_up[_from] += num_pass
            drop_off[to] += num_pass

        current_capacity = 0
        for i in sorted(set([*pick_up.keys()] + [*drop_off.keys()]))
            if i in drop_off
                current_capacity -= drop_off[i]
            if i in pick_up
                current_capacity += pick_up[i]
                if current_capacity > capacity
                    return False
        return True

sol = Solution()

sol.carPooling([[9,1,7],[4,2,4],[9,3,4], [7,4,5]], 23) == true
assert sol.carPooling([[9,1,7],[4,2,4],[9,3,4], [7,4,5]], 23) == true

assert sol.carPooling([[7,5,6],[6,7,8],[10,1,6]],16) == false
assert sol.carPooling([[50, 0, 500], [50, 500, 1000]], 50) == true
assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 4) == false
assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 5) == true
assert sol.carPooling([[1, 0, 1]], 1) == true
assert sol.carPooling([[100, 0, 1000]], 100) == true
assert sol.carPooling([[50, 0, 500], [50, 500, 1000]], 50) == true
assert sol.carPooling([[50, 0, 500], [51, 500, 1000]], 50) == false
assert sol.carPooling([[1, 0, 500], [1, 250, 750], [1, 500, 1000]], 2) == true
assert sol.carPooling([[100, 0, 500], [100, 0, 500], [100, 0, 500]], 300) == true
assert sol.carPooling([[100, 0, 500], [100, 0, 500], [100, 0, 500]], 299) == false
assert sol.carPooling([[1, 0, 1], [1, 1, 2], [1, 2, 3], [1, 3, 4], [1, 4, 5]], 1) == true
assert sol.carPooling([[1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000]], 5) == true
assert sol.carPooling([[100, 0, 1], [100, 1, 2], [100, 2, 3]], 100) == true
assert sol.carPooling([[100, 0, 1], [100, 1, 2], [100, 2, 3]], 99) == false
assert sol.carPooling([[1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000]], 4) == false
