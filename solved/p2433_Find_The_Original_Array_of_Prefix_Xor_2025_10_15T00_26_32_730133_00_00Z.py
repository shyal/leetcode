"""
URL: https://leetcode.com/problems/find-the-original-array-of-prefix-xor/description/

2433. Find The Original Array of Prefix Xor

You are given an integer array pref of size n. Find and return the array arr of size n that satisfies:

        pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i].

Note that ^ denotes the bitwise-xor operation.

It can be proven that the answer is unique.


Example 1:

Input: pref = [5,2,0,3,1]
Output: [5,7,2,3,2]
Explanation: From the array [5,7,2,3,2] we have the following:
- pref[0] = 5.
- pref[1] = 5 ^ 7 = 2.
- pref[2] = 5 ^ 7 ^ 2 = 0.
- pref[3] = 5 ^ 7 ^ 2 ^ 3 = 3.
- pref[4] = 5 ^ 7 ^ 2 ^ 3 ^ 2 = 1.

Example 2:

Input: pref = [13]
Output: [13]
Explanation: We have pref[0] = arr[0] = 13.


Constraints:

        1 <= pref.length <= 105
        0 <= pref[i] <= 106

---

I don't know why this problem is completely frying my brain. I'm so bad at DP it's ridiculous, i look at the xors, and numbers
and my brain freezes. I know this is a super simple DP problem, and yet my brain freezes.

https://leetcode.com/problems/find-the-original-array-of-prefix-xor/solutions/4228796/video-give-me-5-minutes-how-we-think-about-a-solution-python-javascript-java-c/

Revisit.

"""


class Solution:
    def findArray(self, pref: List[int]) -> List[int]:
        # https://leetcode.com/problems/find-the-original-array-of-prefix-xor/solutions/4228796/video-give-me-5-minutes-how-we-think-about-a-solution-python-javascript-java-c/
        # not my solution
        prev = pref[0]
        for i in range(1, len(pref)):
            pref[i] ^= prev
            prev ^= pref[i]
        return pref


sol = Solution()
res = sol.findArray(pref=["a", "b", "c", "d", "e"])
# print(res)
