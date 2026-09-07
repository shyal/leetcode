"""
URL: https://leetcode.com/problems/champagne-tower/description/?envType=problem-list-v2&envId=vn57k9wr

799. Champagne Tower

We stack glasses in a pyramid, where the first row has 1 glass, the second row has 2 glasses, and so on until the 100th row. Each glass holds one cup of champagne.

Then, some champagne is poured into the first glass at the top. When the topmost glass is full, any excess liquid poured will fall equally to the glass immediately to the left and right of it. When those glasses become full, any excess champagne will fall equally to the left and right of those glasses, and so on. (A glass at the bottom row has its excess champagne fall on the floor.)

For example, after one cup of champagne is poured, the top most glass is full. After two cups of champagne are poured, the two glasses on the second row are half full. After three cups of champagne are poured, those two cups become full - there are 3 full glasses total now. After four cups of champagne are poured, the third row has the middle glass half full, and the two outside glasses are a quarter full, as pictured below.

Now after pouring some non-negative integer cups of champagne, return how full the jth glass in the ith row is (both i and j are 0-indexed.)

Example 1:

Input: poured = 1, query_row = 1, query_glass = 1
Output: 0.00000
Explanation: We poured 1 cup of champange to the top glass of the tower (which is indexed as (0, 0)). There will be no excess liquid so all the glasses under the top glass will remain empty.

Example 2:

Input: poured = 2, query_row = 1, query_glass = 1
Output: 0.50000
Explanation: We poured 2 cups of champange to the top glass of the tower (which is indexed as (0, 0)). There is one cup of excess liquid. The glass indexed as (1, 0) and the glass indexed as (1, 1) will share the excess liquid equally, and each will get half cup of champange.

Example 3:

Input: poured = 100000009, query_row = 33, query_glass = 17
Output: 1.00000

Constraints:

    0 <= poured <= 10^9
    0 <= query_glass <= query_row < 100

---

First thing we should find out is, for a given row, how many glasses
are there (including that row).

1: 1
2: 3
3: 6

That's: (n * (n + 1)) // 2

And the number of glasses in that row is query_row.

This is probably a binary search problem. because we want to find the last row n
given poured.

"""


class Solution:
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        def bs():
            low = 0
            high = poured
            result = -1
            is_minimization = True

            while low <= high:
                mid = low + (high - low) // 2
                if (mid * (mid + 1)) // 2 >= poured:
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

        row = bs()
        if query_row <= row:
            return 1
        elif (row * (row + 1)) // 2 < poured < ((row + 1) * (row + 2)):
            return query_row / (poured - (row * (row + 1)) // 2)


sol = Solution()

# print(sol.champagneTower(1, 1, 1))  # 0.0

print(Solution().champagneTower(100, 14, 5))

assert abs(sol.champagneTower(1, 1, 1) - 0.0) < 1e-5
assert abs(sol.champagneTower(2, 1, 1) - 0.5) < 1e-5
assert abs(sol.champagneTower(100000009, 33, 17) - 1.0) < 1e-5

assert Solution().champagneTower(0, 0, 0) == 0.0
assert Solution().champagneTower(1, 0, 0) == 1
assert Solution().champagneTower(10, 4, 2) == 0.625
assert Solution().champagneTower(100, 9, 5) == 1
assert Solution().champagneTower(10**9, 99, 50) == 1
assert Solution().champagneTower(10**9, 99, 99) == 0.0
assert Solution().champagneTower(10**9, 0, 0) == 1
assert Solution().champagneTower(3, 2, 1) == 0.0
assert Solution().champagneTower(4, 2, 0) == 0.25
assert Solution().champagneTower(5, 3, 3) == 0.0
assert Solution().champagneTower(7, 3, 0) == 0.0
assert Solution().champagneTower(15, 5, 2) == 0.875


# FAILED: walked away after 30m 38s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
