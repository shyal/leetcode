"""
URL: https://leetcode.com/problems/minimum-penalty-for-a-shop/description/?envType=problem-list-v2&envId=vn57k9wr

2483. Minimum Penalty for a Shop

You are given the customer visit log of a shop represented by a 0-indexed string customers consisting only of characters 'N' and 'Y':

- if the iᵗʰ character is 'Y', it means that customers come at the iᵗʰ hour
- whereas 'N' indicates that no customers come at the iᵗʰ hour.

If the shop closes at the jᵗʰ hour (0 <= j <= n), the penalty is calculated as follows:

- For every hour when the shop is open and no customers come, the penalty increases by 1.
- For every hour when the shop is closed and customers come, the penalty increases by 1.

Return the earliest hour at which the shop must be closed to incur a minimum penalty.

Note that if a shop closes at the jᵗʰ hour, it means the shop is closed at the hour j.

Example 1:

Input: customers = "YYNY"
Output: 2
Explanation:
- Closing the shop at the 0ᵗʰ hour incurs in 1+1+0+1 = 3 penalty.
- Closing the shop at the 1ˢᵗ hour incurs in 0+1+0+1 = 2 penalty.
- Closing the shop at the 2ⁿᵈ hour incurs in 0+0+0+1 = 1 penalty.
- Closing the shop at the 3ʳᵈ hour incurs in 0+0+1+1 = 2 penalty.
- Closing the shop at the 4ᵗʰ hour incurs in 0+0+1+0 = 1 penalty.
Closing the shop at 2ⁿᵈ or 4ᵗʰ hour gives a minimum penalty. Since 2 is earlier, the optimal closing time is 2.

Example 2:

Input: customers = "NNNNN"
Output: 0
Explanation: It is best to close the shop at the 0ᵗʰ hour as no customers arrive.

Example 3:

Input: customers = "YYYY"
Output: 4
Explanation: It is best to close the shop at the 4ᵗʰ hour as customers arrive at each hour.

Constraints:

    1 <= customers.length <= 10^5
    customers consists only of characters 'Y' and 'N'.
---
def bestClosingTime(customers: str) -> int
  best_hour, best_penalty = 0, inf
  for j in 0..len(customers)
    p = self.penalty(customers, j)
    if p < best_penalty
      best_hour, best_penalty = j, p
  best_hour

Assisted

LEETCODE: Accepted (43 ms, 19.9 MB)
"""


# mu 0.7
# def penalty(customers, j)
#   ret penalty = 0
#   for i in 0..len(customers) - 1
#     if i < j
#       penalty += customers[i] == 'N'
#     else
#       penalty += customers[i] == 'Y'
#
#
# def bestClosingTime(customers: str) -> int
#   p = customers.count('Y')
#   best_hour, best_penalty = 0, p
#   for j in 0..len(customers) - 1
#     if customers[j] == 'Y'
#       p -= 1
#     else
#       p += 1
#     if p < best_penalty
#       best_hour, best_penalty = j + 1, p
#   best_hour

class Solution:
    def penalty(self, customers, j):
        penalty = 0
        for i in range(0, len(customers) - 1 + 1):
            if i < j:
                penalty += customers[i] == 'N'
            else:
                penalty += customers[i] == 'Y'
        return penalty

    def bestClosingTime(self, customers: str) -> int:
        p = customers.count('Y')
        best_hour, best_penalty = 0, p
        for j in range(0, len(customers) - 1 + 1):
            if customers[j] == 'Y':
                p -= 1
            else:
                p += 1
            if p < best_penalty:
                best_hour, best_penalty = j + 1, p
        return best_hour


sol = Solution()
print(sol.bestClosingTime('YYNY'))
assert sol.bestClosingTime('YYNY') == 2
assert sol.bestClosingTime('NNNNN') == 0
assert sol.bestClosingTime('YYYY') == 4
assert sol.bestClosingTime('Y') == 1
assert sol.bestClosingTime('N') == 0
assert sol.bestClosingTime('NYNYNYNYNY') == 0
assert sol.bestClosingTime('YYYYYNNNNN') == 5
assert sol.bestClosingTime('NNNNNYYYYY') == 0
assert sol.bestClosingTime('YNYNYNYNYN') == 1
assert sol.bestClosingTime('N' * 100000) == 0
assert sol.bestClosingTime('Y' * 100000) == 100000
assert sol.bestClosingTime('Y' * 50000 + 'N' * 50000) == 50000
assert sol.bestClosingTime('N' * 50000 + 'Y' * 50000) == 0
assert sol.bestClosingTime('NY' * 50000) == 0
assert sol.bestClosingTime('YN' * 50000) == 1
