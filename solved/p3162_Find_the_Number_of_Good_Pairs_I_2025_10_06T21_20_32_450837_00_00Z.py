"""
URL: https://leetcode.com/problems/find-the-number-of-good-pairs-i/description/?envType=problem-list-v2&envId=vn57k9wr

3162. Find the Number of Good Pairs I

You are given two 0-indexed integer arrays nums1 and nums2 of lengths n and m respectively.

A pair (i, j) is good if:

    nums1[i] == nums2[j]

Return the total number of good pairs.


Example 1:

Input: nums1 = [1,3,4], nums2 = [1,3,4]
Output: 3
Explanation: The good pairs are (0,0), (1,1), and (2,2).

Example 2:

Input: nums1 = [1,2,4,12], nums2 = [2,4]
Output: 2
Explanation: The good pairs are (1,0) and (2,1).

Example 3:

Input: nums1 = [2,1], nums2 = [1,2]
Output: 2
Explanation: The good pairs are (0,1) and (1,0).


Constraints:

    1 <= n, m <= 100
    1 <= nums1[i], nums2[j] <= 100

---

The 5 good pairs are (0, 0), (1, 0), (1, 1), (2, 0), and (2, 2).

"""


class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        count = 0
        for i in range(len(nums1)):
            for j in range(len(nums2)):
                if nums1[i] % (nums2[j] * k) == 0:
                    count += 1
        return count


sol = Solution()

print(sol.numberOfPairs([1, 3, 4], [1, 3, 4], 1))
