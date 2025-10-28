"""
URL: https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/description/?envType=problem-list-v2&envId=vn57k9wr

1760. Minimum Limit of Balls in a Bag

You are given an integer array nums where the i-th bag contains nums[i] balls. You are also given an integer maxOperations.

You can perform the following operation at most maxOperations times:

- Take any bag of balls and divide it into two new bags with a positive number of balls.
  - For example, a bag of 5 balls can become two new bags of 1 and 4 balls, or two new bags of 2 and 3 balls.

Your penalty is the maximum number of balls in a bag. You want to minimize your penalty after the operations.

Return the minimum possible penalty after performing the operations.

Example 1:

Input: nums = [9], maxOperations = 2
Output: 3
Explanation:
- Divide the bag with 9 balls into two bags of sizes 6 and 3. [9] -> [6,3].
- Divide the bag with 6 balls into two bags of sizes 3 and 3. [6,3] -> [3,3,3].
The bag with the most number of balls has 3 balls, so your penalty is 3 and you should return 3.

Example 2:

Input: nums = [2,4,8,2], maxOperations = 4
Output: 2
Explanation:
- Divide the bag with 8 balls into two bags of sizes 4 and 4. [2,4,8,2] -> [2,4,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,4,4,4,2] -> [2,2,2,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,4,4,2] -> [2,2,2,2,2,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,2,2,4,2] -> [2,2,2,2,2,2,2,2].
The bag with the most number of balls has 2 balls, so your penalty is 2, and you should return 2.

Constraints:

- 1 <= nums.length <= 10^5
- 1 <= maxOperations, nums[i] <= 10^9

---

[7, 17], 3 ->

3, 4, 17
3, 4, 11, 6
3, 4, 5, 6, 6

Hint 1:

> Let's change the question if we know the maximum size of a bag what is the minimum number of bags you can make

Ok so we need to flip our thinking here. We guess the maximum size of a bag is 6.. so how do we compute
the minimum number of bags we can make?

Guess = 5
Operations = 3
Bags = [7, 17]

I could try to get 6 from 17, i.e 11 and 6. then same with 11.

So take the max, and subtract 6 to get [7, 11, 6], then do the same with 11..
11-6 = 5, so [7, 5, 6, 6] but surely
it's not that simple to just subtract the guess each time.

Let's try some different numbers:

Guess = 3
Operations = 4
Bags = [5, 5, 5]

We take the max, 5. subtract 3, which leaves us with 3, 2
Do that 3 times to get:

[3,3,3,2,2,2]

On our 4th operation, we can do [3,3,3,0,2,2,2]

Ok let's look at bigger examples now:


Guess = 500000000
Operations = 1
Bags = [1000000000]

We take the max, and subtract 500000000, to get [500000000,500000000]
Ok that works too.

I'll check the second hint to make sure.

> note that as the maximum size increases the minimum number of bags decreases so we can binary search the maximum size

Hmm i have no idea what this means. I think this just means there's an inverse relationship between the max bag and min
number of bags, so it's encouraging us to do a bs.

Hmm i give up because i've overtime. I think i was very close.. but in check_condition, it's not a matter
of subtracting the penalty from the max.

Not my solution.

"""


class Solution:
    def check_condition(self, nums, penalty, max_operations):
        ceil_div = lambda a, b: (a + b - 1) // b
        total_ops = 0
        for x in nums:
            total_ops += ceil_div(x, penalty) - 1
            if total_ops > max_operations:
                return False
        return total_ops <= max_operations

    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        low = 1
        high = max(nums)
        result = -1
        while low <= high:
            mid = low + (high - low) // 2
            if self.check_condition(nums, mid, maxOperations):
                result = mid
                high = mid - 1
            else:
                low = mid + 1
        return result


sol = Solution()

assert sol.minimumSize([9], 2) == 3
assert sol.minimumSize([2, 4, 8, 2], 4) == 2
assert sol.minimumSize([1], 0) == 1
assert sol.minimumSize([1], 1) == 1
assert sol.minimumSize([2], 0) == 2
assert sol.minimumSize([2], 1) == 1
assert sol.minimumSize([1000000000], 0) == 1000000000
assert sol.minimumSize([1000000000], 1) == 500000000
assert sol.minimumSize([7, 17], 3) == 6
assert sol.minimumSize([4, 4], 1) == 4
assert sol.minimumSize([4, 4], 2) == 2
assert sol.minimumSize([3], 1) == 2
assert sol.minimumSize([3], 2) == 1
assert sol.minimumSize([1, 1, 1], 0) == 1
assert sol.minimumSize([1, 1, 1], 10) == 1
assert sol.minimumSize([5, 5, 5], 4) == 3
# assert sol.minimumSize([10, 10], 5) == 2
# assert sol.minimumSize([999999999, 1000000000], 1) == 500000000
assert sol.minimumSize([6], 3) == 2
assert sol.minimumSize([100], 10) == 10
