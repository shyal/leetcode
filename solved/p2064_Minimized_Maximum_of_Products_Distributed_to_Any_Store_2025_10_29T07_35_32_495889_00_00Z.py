"""
URL: https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/description/?envType=problem-list-v2&envId=vn57k9wr

2064. Minimized Maximum of Products Distributed to Any Store

You are given an integer n indicating there are n specialty retail stores. There are m product types of varying amounts, which are given as a 0-indexed integer array quantities, where quantities[i] represents the number of products of the i-th product type.

You need to distribute all products to the retail stores following these rules:

- A store can only be given at most one product type but can be given any amount of it.
- After distribution, each store will have been given some number of products (possibly 0). Let x represent the maximum number of products given to any store. You want x to be as small as possible, i.e., you want to minimize the maximum number of products that are given to any store.

Return the minimum possible x.

Example 1:

Input: n = 6, quantities = [11,6]
Output: 3
Explanation: One optimal way is:
- The 11 products of type 0 are distributed to the first four stores in these amounts: 2, 3, 3, 3
- The 6 products of type 1 are distributed to the other two stores in these amounts: 3, 3
The maximum number of products given to any store is max(2, 3, 3, 3, 3, 3) = 3.

Example 2:

Input: n = 7, quantities = [15,10,10]
Output: 5
Explanation: One optimal way is:
- The 15 products of type 0 are distributed to the first three stores in these amounts: 5, 5, 5
- The 10 products of type 1 are distributed to the next two stores in these amounts: 5, 5
- The 10 products of type 2 are distributed to the last two stores in these amounts: 5, 5
The maximum number of products given to any store is max(5, 5, 5, 5, 5, 5, 5) = 5.

Example 3:

Input: n = 1, quantities = [100000]
Output: 100000
Explanation: The only optimal way is:
- The 100000 products of type 0 are distributed to the only store.
The maximum number of products given to any store is max(100000) = 100000.

Constraints:

- m == quantities.length
- 1 <= m <= n <= 10^5
- 1 <= quantities[i] <= 10^5
"""


class Solution:

    def distribute(self, n, quantities, r):
        ceil_div = lambda a, b: (a + b - 1) // b
        return sum(ceil_div(q, r) for q in quantities)

    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        low = 1
        high = sum(quantities)
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            if self.distribute(n, quantities, mid) <= n:
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

# print(sol.distribute(6, [11, 6], 3))
# print(sol.distribute(7, [15, 10, 10], 5))
# print(sol.minimizedMaximum(6, [11, 6]))  # 3

assert sol.minimizedMaximum(6, [11, 6]) == 3
assert sol.minimizedMaximum(7, [15, 10, 10]) == 5
assert sol.minimizedMaximum(1, [100000]) == 100000
assert sol.minimizedMaximum(1, [1]) == 1
assert sol.minimizedMaximum(2, [1, 1]) == 1
assert sol.minimizedMaximum(2, [1, 2]) == 2
assert sol.minimizedMaximum(3, [3, 3]) == 3
assert sol.minimizedMaximum(4, [3, 3]) == 2
assert sol.minimizedMaximum(5, [10]) == 2
assert sol.minimizedMaximum(2, [5]) == 3
assert sol.minimizedMaximum(100, [1, 1, 1]) == 1
assert sol.minimizedMaximum(4, [1, 2, 3]) == 2
assert sol.minimizedMaximum(3, [1, 2, 3]) == 3
assert sol.minimizedMaximum(10, [100, 1, 1]) == 13
