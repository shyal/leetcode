"""
URL: https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/description/?envType=problem-list-v2&envId=vn57k9wr

1283. Find the Smallest Divisor Given a Threshold

Given an array of integers nums and an integer threshold, we will choose a positive integer divisor, divide all the array by it, and sum the division's result. Find the smallest divisor such that the result mentioned above is less than or equal to threshold.

Each result of the division is rounded to the nearest integer greater than or equal to that element. (For example: 7/3 = 3 and 10/2 = 5).

The test cases are generated so that there will be an answer.

Example 1:

Input: nums = [1,2,5,9], threshold = 6
Output: 5
Explanation: We can get a sum to 17 (1+2+5+9) if the divisor is 1.
If the divisor is 4 we can get a sum of 7 (1+1+2+3) and if the divisor is 5 the sum will be 5 (1+1+1+2).

Example 2:

Input: nums = [44,22,33,11,1], threshold = 5
Output: 44

Constraints:

    1 <= nums.length <= 5 * 10^4
    1 <= nums[i] <= 10^6
    nums.length <= threshold <= 10^6

---

Super easy thanks to bs minimization template.

"""


class Solution:
    # @viz_binary_search()
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        low = 1
        high = sum(nums)
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            condition = sum([ceil(x / mid) for x in nums])
            if condition <= threshold:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if is_minimization:
                    low = mid + 1
                else:
                    high = mid - 1

        return result


sol = Solution()

# print(sol.smallestDivisor([1, 2, 5, 9], 6))  # 5

assert sol.smallestDivisor([1, 2, 5, 9], 6) == 5
assert sol.smallestDivisor([44, 22, 33, 11, 1], 5) == 44
assert sol.smallestDivisor([1], 1) == 1
assert sol.smallestDivisor([1000000], 1) == 1000000
assert sol.smallestDivisor([1, 2, 3], 6) == 1
assert sol.smallestDivisor([1, 2, 3], 5) == 2
assert sol.smallestDivisor([5, 5, 5, 5], 8) == 3
assert sol.smallestDivisor([9, 3], 3) == 5
assert sol.smallestDivisor([2, 3, 5, 7, 11], 11) == 3
assert sol.smallestDivisor([1, 2], 2) == 2
assert sol.smallestDivisor([1, 1], 2) == 1
