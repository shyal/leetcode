"""
URL: https://leetcode.com/problems/car-pooling/description/?envType=problem-list-v2&envId=vn57k9wr

1094. Car Pooling

There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where trips[i] = [numPassengers_i, from_i, to_i] indicates that the i-th trip has numPassengers_i passengers and the locations to pick them up and drop them off are from_i and to_i respectively. The locations are given as the number of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise.

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
"""


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        _from = defaultdict(int)
        _to = defaultdict(int)
        kms = set([])
        for n, f, t in trips:
            _from[f] += n
            _to[t] -= n
            kms.add(f)
            kms.add(t)

        total = 0
        for k in sorted(list(kms)):
            total += _from[k]
            total += _to[k]
            if total > capacity:
                return False
        return True


sol = Solution()

# print(sol.carPooling([[2, 1, 5], [3, 3, 7]], 4))  # False

# assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 4) == False
assert sol.carPooling([[2, 1, 5], [3, 3, 7]], 5) == True

assert sol.carPooling([[1, 0, 1]], 1) == True
assert sol.carPooling([[100, 0, 1000]], 100) == True
assert sol.carPooling([[50, 0, 500], [50, 500, 1000]], 50) == True
assert sol.carPooling([[50, 0, 500], [51, 500, 1000]], 50) == False
assert sol.carPooling([[1, 0, 500], [1, 250, 750], [1, 500, 1000]], 2) == True
assert sol.carPooling([[100, 0, 500], [100, 0, 500], [100, 0, 500]], 300) == True
assert sol.carPooling([[100, 0, 500], [100, 0, 500], [100, 0, 500]], 299) == False
assert (
    sol.carPooling([[1, 0, 1], [1, 1, 2], [1, 2, 3], [1, 3, 4], [1, 4, 5]], 1) == True
)
assert (
    sol.carPooling(
        [[1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000]], 5
    )
    == True
)
assert sol.carPooling([[100, 0, 1], [100, 1, 2], [100, 2, 3]], 100) == True
assert sol.carPooling([[100, 0, 1], [100, 1, 2], [100, 2, 3]], 99) == False
assert (
    sol.carPooling(
        [[1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000], [1, 0, 1000]], 4
    )
    == False
)
