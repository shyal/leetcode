"""
URL: https://leetcode.com/problems/minimum-operations-to-convert-number/description/?envType=problem-list-v2&envId=vn57k9wr

2059. Minimum Operations to Convert Number

You are given a 0-indexed integer array nums containing distinct numbers, an integer start, and an integer goal. There is an integer x that is initially set to start, and you want to perform operations on x such that it is converted to goal. You can perform the following operation repeatedly on the number x:

If 0 <= x <= 1000, then for any index i in the array (0 <= i < nums.length), you can set x to any of the following:

- x + nums[i]
- x - nums[i]
- x ^ nums[i] (bitwise-XOR)

Note that you can use each nums[i] any number of times in any order. Operations that set x to be out of the range 0 <= x <= 1000 are valid, but no more operations can be done afterward.

Return the minimum number of operations needed to convert x = start into goal, and -1 if it is not possible.

Example 1:

Input: nums = [2,4,12], start = 2, goal = 12
Output: 2
Explanation: We can go from 2 → 14 → 12 with the following 2 operations.
- 2 + 12 = 14
- 14 - 2 = 12

Example 2:

Input: nums = [3,5,7], start = 0, goal = -4
Output: 2
Explanation: We can go from 0 → 3 → -4 with the following 2 operations.
- 0 + 3 = 3
- 3 - 7 = -4
Note that the last operation sets x out of the range 0 <= x <= 1000, which is valid.

Example 3:

Input: nums = [2,8,16], start = 0, goal = 1
Output: -1
Explanation: There is no way to convert 0 into 1.

Constraints:

    1 <= nums.length <= 1000
    -10^9 <= nums[i], goal <= 10^9
    0 <= start <= 1000
    start != goal
    All the integers in nums are distinct.

---

Hmm using a combinations approach has a huge solution space
so either DP or greedy.

If the goal is bigger than x, we need to add.
If the goal is small than x, we need to sub or xor.

I'll probably try recursive with caching..


x = start
for n in nums:
    add = x + n
    sub = x - n
    xor = x ^ n
    print(f"add: {add}, sub: {sub}, xor: {xor}")

This gives us:

add: 4, sub: 0, xor: 0
add: 6, sub: -2, xor: 6
add: 14, sub: -10, xor: 14

We're closer than we were at the start: 2 -> 14, so add was the right step

Fail.

"""


class Solution:
    def minimumOperations(self, nums: List[int], start: int, goal: int) -> int:
        x = start
        best = []
        for n in nums:
            add = x + n
            sub = x - n
            xor = x ^ n
            print(f"add: {add}, sub: {sub}, xor: {xor}")
            res = [
                (abs(add - goal), add),
                (abs(sub - goal), sub),
                (abs(xor - goal), xor),
            ]
            print(min(abs(add - goal), abs(sub - goal), abs(xor - goal)))
            res.sort()
            print(res)
            # x = res[0][0]
            print("cand", res[0][1])
            # print("------")
            best.append(res[0])

        print(best)


sol = Solution()

print(sol.minimumOperations([2, 4, 12], 2, 12))  # 2

# assert sol.minimumOperations([2, 4, 12], 2, 12) == 2
# assert sol.minimumOperations([3, 5, 7], 0, -4) == 2
# assert sol.minimumOperations([2, 8, 16], 0, 1) == -1

# assert sol.minimumOperations([1], 0, 1000) == 1000
# assert sol.minimumOperations([1000], 1000, 0) == 1
# assert sol.minimumOperations([0], 500, 500) == 0
# assert sol.minimumOperations([1, 2, 3], 0, -1000000000) == -1
# assert sol.minimumOperations([1, 2, 3], 0, 1000000000) == -1
# assert sol.minimumOperations([1, 1, 1], 0, 3) == 3
# assert sol.minimumOperations([999], 0, 999) == 1
# assert sol.minimumOperations([500, 500], 0, 1000) == 2
# assert sol.minimumOperations([1, 2, 3], 1000, 0) == 334
# assert sol.minimumOperations([10**9], 0, 10**9) == 1
# assert sol.minimumOperations([-1, -2, -3], 0, -6) == 3
# assert sol.minimumOperations([0, 1, 2], 0, 2) == 1


# FAILED: walked away after 26m 59s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
