"""
URL: https://leetcode.com/problems/magnetic-force-between-two-balls/description/?envType=problem-list-v2&envId=vn57k9wr

1552. Magnetic Force Between Two Balls

In the universe Earth C-137, Rick discovered a special form of magnetic force between two balls if they are put in his new invented basket. Rick has n empty baskets, the i-th basket is at position[i], Morty has m balls and needs to distribute the balls into the baskets such that the minimum magnetic force between any two balls is maximum.

Rick stated that magnetic force between two different balls at positions x and y is |x - y|.

Given the integer array position and the integer m. Return the required force.

Example 1:

Input: position = [1,2,3,4,7], m = 3
Output: 3
Explanation: Distributing the 3 balls into baskets 1, 4 and 7 will make the magnetic force between ball pairs [3, 3, 6]. The minimum magnetic force is 3. We cannot achieve a larger minimum magnetic force than 3.

Example 2:

Input: position = [5,4,3,2,1,1000000000], m = 2
Output: 999999999
Explanation: We can use baskets 1 and 1000000000.

Constraints:

    n == position.length
    2 <= n <= 10^5
    1 <= position[i] <= 10^9
    All integers in position are distinct.
    2 <= m <= position.length

---

Tricky problem. I think the first step is to place the balls in an equidistant manner. Let's illustrate to see if this helps.

o     o     o
- - - -     -
1 2 3 4     7

So by placing the balls in 1, 4 and 7, they're equidistant. The min is the min distance between any two balls.
We could verify this by checking the distance between any 2 balls.

Now to place the balls, we could think of an approach where, for example, we place a ball at P[0], then at P[-1],
then at the equidistant position between 1 and 7, which happens to be a free slot (4).

Placing the balls will be difficult, but since we know we're looking for the maximum minimum distance,
we can try placing a guess, i.e use binary search.

# a dist a 4 cannot fit
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=4, num_balls=3) == False

# a dist of 3, and 2 fit, and clearly 3 > 2
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=3, num_balls=3) == True
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=2, num_balls=3) == True

Great so if we turn the positions into a heap, we can efficiently greedily place
the balls.

Hmm tried submitting, sadly not the right answer. For some reason the template
is not maximizing properly.

Solved! Just needed to choose generous bounds.
"""


class Solution:

    def canPlaceBalls(self, position, min_dist, num_balls):
        position = position[:]
        heapify(position)
        placements = []
        while position:
            top = heappop(position)
            if not placements:
                placements.append(top)
            else:
                dist = top - placements[-1]
                if dist >= min_dist:
                    placements.append(top)
            if len(placements) >= num_balls:
                return True
        return len(placements) >= num_balls

    # @viz_binary_search()
    def maxDistance(self, position: List[int], m: int) -> int:
        low = 1
        high = max(position)
        result = -1
        is_minimization = False

        while low <= high:
            min_dist = low + (high - low) // 2
            if self.canPlaceBalls(position, min_dist, m):
                result = min_dist
                if is_minimization:
                    high = min_dist - 1
                else:
                    low = min_dist + 1
            else:
                if is_minimization:
                    low = min_dist + 1
                else:
                    high = min_dist - 1

        return result


sol = Solution()


# a dist a 4 cannot fit
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=4, num_balls=3) == False

# a dist of 3, and 2 fit, and clearly 3 > 2
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=3, num_balls=3) == True
assert sol.canPlaceBalls(position=[1, 2, 3, 4, 7], min_dist=2, num_balls=3) == True

assert sol.canPlaceBalls(position=[79, 74, 57, 22], min_dist=5, num_balls=4) == True
assert sol.canPlaceBalls(position=[79, 74, 57, 22], min_dist=4, num_balls=4) == True
assert sol.canPlaceBalls(position=[79, 74, 57, 22], min_dist=6, num_balls=4) == False


assert sol.maxDistance([1, 2, 3, 4, 7], 3) == 3
assert sol.maxDistance([5, 4, 3, 2, 1, 1000000000], 2) == 999999999
assert sol.maxDistance([1, 2], 2) == 1
assert sol.maxDistance([1, 3, 10], 3) == 2
assert sol.maxDistance([1, 1000000000], 2) == 999999999
assert sol.maxDistance([1, 2, 3, 4], 4) == 1
assert sol.maxDistance([10, 1, 5], 2) == 9
assert sol.maxDistance([1, 2, 4, 10], 4) == 1
assert sol.maxDistance([1, 100, 101, 200], 3) == 99
assert sol.maxDistance([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 2
assert sol.maxDistance(position=[79, 74, 57, 22], m=4) == 5
