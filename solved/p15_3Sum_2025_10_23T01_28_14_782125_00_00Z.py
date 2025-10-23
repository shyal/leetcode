"""
URL: https://leetcode.com/problems/3sum/description/

15. 3Sum

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.


Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.


Constraints:

    3 <= nums.length <= 3000
    -105 <= nums[i] <= 105

---

I'm not sure why, but i had to peek at the solution for this. Clearly something
isn't sticking, so let's go over this step by step.

First of all, we sort nums. I'm guessing this is because we want to avoid duplicate
triplets, but i'm not 100% sure about that.

We use a set for our result, and a set to track what has been seen.

We start with an i iterator over the entire list.

 i
[1, -1, 0, 5, -5]

if i > 0 and nums[i] == nums[i - 1]:
    continue

I think this is to skip over the possibility of duplicate triplets, but will
have to confirm if this is really needed.

Next, the target is -nums[i], which makes sense, because we're now performing
a two sum, and that's our target.

Next we iterate from i + 1 to the len of nums, which also makes sense.

Our complement is: complement = target - nums[j] which also makes sense.

 i   j
[1, -1, 0, 5, -5]

complement = -1 - (-1)
i.e 0

The complement is minus i, and if we take away what's at j, we get 0,
meaning if we encouter 0 we'll have a triplet.

So if the complement is in d, we add the triplet to res.

Finally we add nums[j] to our seen set, for our complement matching
later.

Reschedule.

"""


class Solution:

    def twoSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        D = defaultdict(int)
        D[0] = 1
        target = 0
        for j in range(len(nums)):
            complement = target - nums[j]
            if complement in D:
                res.append([complement, nums[j]])
                D[complement] += 1
            D[nums[j]] += 1
        return res

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set([])
        D = set()
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            target = -nums[i]
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in D:
                    res.add((nums[i], complement, nums[j]))
                D.add(nums[j])
        return [list(x) for x in sorted(res)]


sol = Solution()

res = sol.threeSum([1, 1, -1, 0, 5, -5])
# print(res)


# assert sol.threeSum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
# assert sol.threeSum([0, 1, 1]) == []
# assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]
# assert sol.threeSum([1, 2, -3]) == [[-3, 1, 2]]
# assert sol.threeSum([-2, 0, 2]) == [[-2, 0, 2]]
# assert sol.threeSum([0, 0, 1]) == []
# assert sol.threeSum([-1, 1, 0]) == [[-1, 0, 1]]
# assert sol.threeSum([1, 1, 1]) == []
# assert sol.threeSum([-4, -2, -2, -2, 0, 1, 2, 2, 4]) == [[-4, 2, 2], [-2, 0, 2], [-4, 0, 4], [-2, -2, 4]]
# assert sol.threeSum([3, 3, -3, -3, -6, -6]) == [[-6, 3, 3]]
# assert sol.threeSum([100000, -50000, -50000]) == [[-50000, -50000, 100000]]
# assert sol.threeSum([1, -1, 3]) == []
# assert sol.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
# assert sol.threeSum([-1, -2, -3]) == []
# assert sol.threeSum([-1, -1, -1, 1, 1, 1]) == []
