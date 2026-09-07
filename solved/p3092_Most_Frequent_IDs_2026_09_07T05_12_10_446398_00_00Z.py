"""
URL: https://leetcode.com/problems/most-frequent-ids/description/?envType=problem-list-v2&envId=vn57k9wr

3092. Most Frequent IDs

Given two integer arrays nums and freq of the same length n, return an array ans of length n, where ans[i] is the count of the most frequent ID in the collection after step i.

The collection starts empty. At step i, the array nums gives an ID and the array freq says what happens to it. If freq[i] is positive, add freq[i] copies of nums[i] to the collection. If freq[i] is negative, remove -freq[i] copies of nums[i] from the collection. If the collection is empty after step i, then ans[i] is 0.

Example 1:

Input: nums = [2,3,2,1], freq = [3,2,-3,1]
Output: [3,3,2,2]
Explanation:
After step 0 the collection holds 3 copies of 2, so ans[0] = 3.
After step 1 it holds 3 copies of 2 and 2 copies of 3, so ans[1] = 3.
After step 2 it holds 2 copies of 3, so ans[2] = 2.
After step 3 it holds 2 copies of 3 and 1 copy of 1, so ans[3] = 2.

Example 2:

Input: nums = [5,5,3], freq = [2,-2,1]
Output: [2,0,1]
Explanation:
After step 0 the collection holds 2 copies of 5, so ans[0] = 2.
After step 1 the collection is empty, so ans[1] = 0.
After step 2 it holds 1 copy of 3, so ans[2] = 1.

Constraints:

    1 <= nums.length == freq.length <= 10^5
    1 <= nums[i] <= 10^5
    -10^5 <= freq[i] <= 10^5
    freq[i] != 0
    The input never removes more copies of an ID than the collection holds.

---

This question made zero sense.

"""


class Solution:
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        col = defaultdict(int)
        res = []
        for n, f in zip(nums, freq):
            col[n] += f
            if col[n] <= 0:
                del col[n]
            res.append(max(col.values()) if col else 0)
        return res


sol = Solution()

print(sol.mostFrequentIDs([2, 3, 2, 1], [3, 2, -3, 1]))  # [3,3,2,2]

assert sol.mostFrequentIDs([2, 3, 2, 1], [3, 2, -3, 1]) == [3, 3, 2, 2]
assert sol.mostFrequentIDs([5, 5, 3], [2, -2, 1]) == [2, 0, 1]

assert sol.mostFrequentIDs([1], [1]) == [1]
assert sol.mostFrequentIDs([1], [-1]) == [0]
assert sol.mostFrequentIDs([1, 1, 1], [1, 1, -2]) == [1, 2, 0]
assert sol.mostFrequentIDs([1, 2, 3, 4, 5], [1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1]
assert sol.mostFrequentIDs(
    [1, 2, 3, 4, 5], [100000, 100000, 100000, 100000, 100000]
) == [100000, 100000, 100000, 100000, 100000]
assert sol.mostFrequentIDs([1, 1, 2, 2, 3, 3], [1, -1, 1, -1, 1, -1]) == [
    1,
    0,
    1,
    0,
    1,
    0,
]
assert sol.mostFrequentIDs([1, 2, 1, 2, 1, 2], [1, 1, -1, -1, 1, 1]) == [
    1,
    1,
    1,
    0,
    1,
    1,
]
assert sol.mostFrequentIDs([10**5] * 3, [10**5, -(10**5), 10**5]) == [100000, 0, 100000]
assert sol.mostFrequentIDs([1, 2, 3, 4, 5], [1, -1, 1, -1, 1]) == [1, 1, 1, 1, 1]
assert sol.mostFrequentIDs([1] * 5, [1, 1, 1, 1, -5]) == [1, 2, 3, 4, 0]
assert sol.mostFrequentIDs([1, 2, 3, 4, 5], [1, 2, 3, -3, -3]) == [1, 2, 3, 3, 3]
assert sol.mostFrequentIDs(
    [1, 2, 3, 4, 5], [10**5, -(10**5), 10**5, -(10**5), 10**5]
) == [100000, 100000, 100000, 100000, 100000]
