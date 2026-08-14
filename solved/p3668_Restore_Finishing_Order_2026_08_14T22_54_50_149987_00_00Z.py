"""
URL: https://leetcode.com/problems/restore-finishing-order/description/?envType=problem-list-v2&envId=vn57k9wr

3668. Restore Finishing Order

You are given an integer array order of length n and an integer array friends.

    - order contains every integer from 1 to n exactly once, representing the
      IDs of the participants of a race in their finishing order.
    - friends contains the IDs of your friends in the race sorted in strictly
      increasing order. Each ID in friends is guaranteed to appear in the
      order array.

Return an array containing your friends' IDs in their finishing order.


Example 1:

Input: order = [3,1,2,5,4], friends = [1,3,4]
Output: [3,1,4]
Explanation: The finishing order is [3, 1, 2, 5, 4]. Therefore, the finishing
order of your friends is [3, 1, 4].

Example 2:

Input: order = [1,4,5,3,2], friends = [2,5]
Output: [5,2]
Explanation: The finishing order is [1, 4, 5, 3, 2]. Therefore, the finishing
order of your friends is [5, 2].


Constraints:

    1 <= n == order.length <= 100
    order contains every integer from 1 to n exactly once
    1 <= friends.length <= min(8, n)
    1 <= friends[i] <= n
    friends is strictly increasing
"""


class Solution:
    def recoverOrder(self, order: List[int], friends: List[int]) -> List[int]:
        friends = set(friends)
        return [o for o in order if o in friends]


sol = Solution()

print(sol.recoverOrder([3, 1, 2, 5, 4], [1, 3, 4]))  # [3, 1, 4]

assert sol.recoverOrder([3, 1, 2, 5, 4], [1, 3, 4]) == [3, 1, 4]
assert sol.recoverOrder([1, 4, 5, 3, 2], [2, 5]) == [5, 2]
assert sol.recoverOrder([1], [1]) == [1]
assert sol.recoverOrder([2, 1], [1]) == [1]
assert sol.recoverOrder([2, 1], [2]) == [2]
assert sol.recoverOrder([2, 1], [1, 2]) == [2, 1]
assert sol.recoverOrder([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
assert sol.recoverOrder([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
assert sol.recoverOrder([4, 2, 1, 3], [3]) == [3]
assert sol.recoverOrder([3, 1, 2, 5, 4], [2, 5]) == [2, 5]
assert sol.recoverOrder([7, 3, 5, 1, 6, 2, 4], [4, 7]) == [7, 4]
assert sol.recoverOrder([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 3, 5, 7, 9]) == [9, 7, 5, 3, 1]
assert sol.recoverOrder([8, 1, 7, 2, 6, 3, 5, 4], [1, 2, 3, 4, 5, 6, 7, 8]) == [8, 1, 7, 2, 6, 3, 5, 4]
assert sol.recoverOrder(list(range(1, 101)), [1, 25, 50, 75, 100]) == [1, 25, 50, 75, 100]
assert sol.recoverOrder(list(range(100, 0, -1)), [1, 25, 50, 75, 100]) == [100, 75, 50, 25, 1]