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

I appreciate being pushed into the deep end like this, but
this still feels hard.

"""


class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        pass


sol = Solution()

# print(sol.maxDistance([1,2,3,4,7], 3))  # 3

# assert sol.maxDistance([1,2,3,4,7], 3) == 3
# assert sol.maxDistance([5,4,3,2,1,1000000000], 2) == 999999999
# assert sol.maxDistance([1,2], 2) == 1
# assert sol.maxDistance([1,3,10], 3) == 2
# assert sol.maxDistance([1,1000000000], 2) == 999999999
# assert sol.maxDistance([1,2,3,4], 4) == 1
# assert sol.maxDistance([10,1,5], 2) == 9
# assert sol.maxDistance([1,2,4,10], 4) == 1
# assert sol.maxDistance([1,100,101,200], 3) == 99
# assert sol.maxDistance([1,2,3,4,5,6,7,8,9,10], 5) == 2
