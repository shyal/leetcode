"""
URL: https://leetcode.com/problems/k-closest-points-to-origin/description/

973. K Closest Points to Origin

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).


Example 1:

Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].

Example 2:

Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.


Constraints:

        1 <= k <= points.length <= 104
        -104 <= xi, yi <= 104
"""


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for x, y in points:
            d = -sqrt(x * x + y * y)
            if len(heap) < k:
                heappush(heap, (d, [x, y]))
            else:
                if d > heap[0][0]:
                    heappop(heap)
                    heappush(heap, (d, [x, y]))
        draw_heap(heap)
        return [x[1] for x in nlargest(k, heap)]


sol = Solution()

assert sorted(sol.kClosest([[1, 3], [-2, 2]], 1)) == sorted([[-2, 2]])
assert sorted(sol.kClosest([[3, 3], [5, -1], [-2, 4]], 2)) == sorted([[3, 3], [-2, 4]])
assert sorted(sol.kClosest([[0, 0]], 1)) == sorted([[0, 0]])
assert sorted(sol.kClosest([[0, 0], [1, 0], [2, 0], [3, 0]], 4)) == sorted(
    [[0, 0], [1, 0], [2, 0], [3, 0]]
)
assert sorted(sol.kClosest([[-5, 3], [4, -2], [0, 0]], 2)) == sorted([[0, 0], [4, -2]])
assert sorted(sol.kClosest([[1, 0]], 1)) == sorted([[1, 0]])
assert sorted(
    sol.kClosest([[10000, 10000], [-10000, 0], [0, 0], [5000, 5000]], 3)
) == sorted([[0, 0], [-10000, 0], [5000, 5000]])
