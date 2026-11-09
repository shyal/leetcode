"""
EPI 10.4 Compute the k closest stars

Given an iterator stars of Star objects and an integer k, return a list
of the k stars nearest to the origin (0, 0, 0), in any order. The
attribute star.distance holds the distance of a star from the origin.
Two stars compare by distance: a < b is a.distance < b.distance.

Example 1:

Input: stars = iter([Star(3, 4, 0), Star(1, 1, 1), Star(0, 0, 10), Star(2, 0, 0)]), k = 2
Output: [Star(1, 1, 1), Star(2, 0, 0)]
Explanation: the distances are 5, 1.73, 10 and 2.

Example 2:

Input: stars = iter([Star(0, 0, 1)]), k = 1
Output: [Star(0, 0, 1)]

Example 3:

Input: stars = iter([Star(1, 0, 0), Star(0, 5, 0), Star(0, 0, 2)]), k = 3
Output: [Star(1, 0, 0), Star(0, 5, 0), Star(0, 0, 2)]

Constraints:

    1 <= k <= n <= 10^5, where n is the number of stars
    -10^6 <= x, y, z <= 10^6
    No two stars have the same distance.

    REQUIRED: O(n log k) time and O(k) extra space. NO sorted(), NO
    list.sort(), NO heapq.nsmallest(), NO list(stars).
"""


class Star:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z
        self.distance = sqrt(x * x + y * y + z * z)

    def __lt__(self, other) -> bool:
        return self.distance < other.distance

    def __repr__(self) -> str:
        return f"Star({self.x}, {self.y}, {self.z})"


class Solution:
    def find_closest_k_stars(self, stars: Iterator[Star], k: int) -> list[Star]:
        pass


sol = Solution()

print(sol.find_closest_k_stars(iter([Star(3, 4, 0), Star(1, 1, 1), Star(0, 0, 10), Star(2, 0, 0)]), 2))  # [Star(1, 1, 1), Star(2, 0, 0)] in any order

# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(3, 4, 0), Star(1, 1, 1), Star(0, 0, 10), Star(2, 0, 0)]), 2)) == [(1, 1, 1), (2, 0, 0)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(0, 0, 1)]), 1)) == [(0, 0, 1)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(1, 0, 0), Star(0, 5, 0), Star(0, 0, 2)]), 3)) == [(0, 0, 2), (0, 5, 0), (1, 0, 0)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(1, 0, 0), Star(0, 5, 0), Star(0, 0, 2)]), 1)) == [(1, 0, 0)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(9, 0, 0), Star(0, 8, 0), Star(0, 0, 7)]), 1)) == [(0, 0, 7)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(0, 0, 0), Star(10, 10, 10), Star(-1, -1, 0)]), 2)) == [(-1, -1, 0), (0, 0, 0)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(-6, 0, 0), Star(5, 0, 0), Star(0, -4, 0), Star(0, 0, 3)]), 2)) == [(0, -4, 0), (0, 0, 3)]
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter([Star(0.5, 0, 0), Star(0, 0.25, 0)]), 1)) == [(0, 0.25, 0)]
# assert len(sol.find_closest_k_stars(iter([Star(i, 0, 0) for i in range(1, 11)]), 4)) == 4
# assert sorted((s.x, s.y, s.z) for s in sol.find_closest_k_stars(iter(Star(i, 0, 0) for i in range(10 ** 5, 0, -1)), 3)) == [(1, 0, 0), (2, 0, 0), (3, 0, 0)]
# assert sorted(s.x for s in sol.find_closest_k_stars(iter(Star(0, i, 0) if i % 2 else Star(i, 0, 0) for i in range(1, 10 ** 5 + 1)), 10 ** 5)) == [0] * 50000 + list(range(2, 10 ** 5 + 1, 2))
# assert sorted(s.distance for s in sol.find_closest_k_stars(iter(Star(i * 7919 % 10 ** 5, 0, 0) for i in range(10 ** 5)), 5)) == [0, 1, 2, 3, 4]
