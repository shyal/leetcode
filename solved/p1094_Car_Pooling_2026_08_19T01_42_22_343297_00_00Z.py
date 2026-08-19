"""
URL: https://leetcode.com/problems/car-pooling/description/?envType=problem-list-v2&envId=vn57k9wr

1094. Car Pooling

There is a car with capacity empty seats. The vehicle only drives east
(i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where
trips[i] = [numPassengers_i, from_i, to_i] indicates that the ith trip has
numPassengers_i passengers and the locations to pick them up and drop them
off are from_i and to_i respectively. The locations are given as the number
of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for
all the given trips, or false otherwise.


Example 1:

Input: trips = [[2,1,5],[3,3,7]], capacity = 4
Output: false

Example 2:

Input: trips = [[2,1,5],[3,3,7]], capacity = 5
Output: true


Constraints:

    1 <= trips.length <= 1000
    trips[i].length == 3
    1 <= numPassengers_i <= 100
    0 <= from_i < to_i <= 1000
    1 <= capacity <= 10^5

---
                    km due east from car's initial location
                                    v

              num pass      pick up   drop off

trips[i] = [numPassengers_i, from_i, to_i]

capacity 4

          3----------------7
  2---------------5

  1.  2.  3.  4.  5.  6.   7

"""


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        pick_up = defaultdict(int)
        drop_off = defaultdict(int)

        for num_pass, _from, to in trips:
            pick_up[_from] += num_pass
            drop_off[to] += num_pass

        current_capacity = 0
        for i in sorted(set([*pick_up.keys()] + [*drop_off.keys()])):
            if i in drop_off:
                current_capacity -= drop_off[i]
            if i in pick_up:
                current_capacity += pick_up[i]
                if current_capacity > capacity:
                    return False
        return True



sol = Solution()

print(sol.carPooling([[2, 1, 5], [3, 3, 7]], 4))  # False

assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 4) == False
assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 5) == True
assert sol.carPooling([[2, 1, 5], [3, 5, 7]], 3) == True
assert sol.carPooling([[3, 2, 5], [3, 5, 7]], 3) == True
assert sol.carPooling([[5, 0, 1]], 4) == False
assert sol.carPooling([[5, 0, 1]], 5) == True
assert sol.carPooling([[100, 0, 1000]], 100) == True
assert sol.carPooling([[100, 0, 1000]], 99) == False
assert sol.carPooling([[10, 999, 1000]], 10) == True
assert sol.carPooling([[1, 0, 5], [1, 0, 5], [1, 0, 5]], 2) == False
assert sol.carPooling([[1, 0, 5], [1, 0, 5], [1, 0, 5]], 3) == True
assert sol.carPooling([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11) == True
assert sol.carPooling([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 10) == False
assert sol.carPooling([[4, 0, 3], [4, 3, 6], [4, 6, 9]], 4) == True
assert sol.carPooling([[4, 0, 3], [4, 3, 6], [4, 6, 9]], 3) == False
assert sol.carPooling([[100, 0, 1], [100, 0, 1]], 200) == True
assert sol.carPooling([[100, 0, 1], [100, 0, 1]], 199) == False
assert sol.carPooling([[9, 0, 1], [3, 3, 7]], 9) == True
assert sol.carPooling([[9, 0, 1], [3, 3, 7]], 8) == False
assert sol.carPooling([[1, 0, 1000]], 100000) == True
assert sol.carPooling([[2, 1, 3], [2, 2, 4], [2, 3, 5]], 4) == True
assert sol.carPooling([[2, 1, 3], [2, 2, 4], [2, 3, 5]], 3) == False