from typing import List

"""
URL: https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/description/?envType=problem-list-v2&envId=vn57k9wr

1475. Final Prices With a Special Discount in a Shop

You are given an integer array prices where prices[i] is the price of the ith item in a shop.

There is a special discount for items in the shop: If you buy the ith item, then you will receive a discount equivalent to prices[j] where j is the minimum index such that j > i and prices[j] <= prices[i], otherwise, you will not receive any discount at all.

Return an array where the ith element is the final price you will pay for the ith item of the shop considering the special discount.


Example 1:

Input: prices = [8,4,6,2,3]
Output: [4,2,4,2,3]
Explanation: 
For item 0 with price[0]=8 you will receive a discount equivalent to prices[1]=4, therefore, the final price is 8 - 4 = 4.
For item 1 with price[1]=4 you will receive a discount equivalent to prices[3]=2, therefore, the final price is 4 - 2 = 2.
For item 2 with price[2]=6 you will receive a discount equivalent to prices[3]=2, therefore, the final price is 6 - 2 = 4.
For items 3 and 4 there is no discount at all.

Example 2:

Input: prices = [1,2,3,4,5]
Output: [1,2,3,4,5]
Explanation: In this case, for all items, there is no discount at all.

Example 3:

Input: prices = [10,1,1,6]
Output: [9,0,1,6]


Constraints:

    1 <= prices.length <= 500
    1 <= prices[i] <= 1000

"""


class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        res = []
        for i, p in enumerate(prices):
            disc = next(filter(lambda x: x <= p, prices[i + 1 :]), None)
            res.append(p - disc if disc is not None else p)
        return res


sol = Solution()

# print(sol.finalPrices([8, 4, 6, 2, 3]))  # [4,2,4,2,3]

assert sol.finalPrices([8, 4, 6, 2, 3]) == [4, 2, 4, 2, 3]
assert sol.finalPrices([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
assert sol.finalPrices([10, 1, 1, 6]) == [9, 0, 1, 6]
assert sol.finalPrices([1]) == [1]
assert sol.finalPrices([1, 1]) == [0, 1]
assert sol.finalPrices([2, 1]) == [1, 1]
assert sol.finalPrices([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]
assert sol.finalPrices([5, 5, 5]) == [0, 0, 5]
assert sol.finalPrices([1000, 1, 1]) == [999, 0, 1]
assert sol.finalPrices([1, 1, 1, 1]) == [0, 0, 0, 1]
