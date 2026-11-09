"""
EPI 16.6 The knapsack problem

Given a list items and an integer capacity, return the largest total
value of a set of items whose total weight is at most capacity. Each
item has a weight, item.weight, and a value, item.value. Each item goes
in the set at most once.

Example 1:

Input: items = [Item(5, 60), Item(3, 50), Item(4, 70), Item(2, 30)],
       capacity = 5
Output: 80
Explanation: the items of weight 3 and 2. The item of weight 4 alone
has the most value per unit of weight and gives 70.

Example 2:

Input: items = [Item(5, 60), Item(3, 50), Item(4, 70), Item(2, 30)],
       capacity = 9
Output: 150
Explanation: the items of weight 3, 4 and 2.

Example 3:

Input: items = [Item(3, 7)], capacity = 2
Output: 0
Explanation: the item does not fit.

Constraints:

    1 <= len(items) <= 100
    1 <= item.weight, item.value <= 1000
    0 <= capacity <= 1000
    Item(weight, value) is a named tuple.

    REQUIRED: O(len(items) * capacity) time. NO most-value-per-weight
    first. NO enumeration of every subset of the items.
"""

Item = collections.namedtuple("Item", ("weight", "value"))


class Solution:
    def optimum_subject_to_capacity(self, items: list[Item], capacity: int) -> int:
        pass


sol = Solution()


def as_items(pairs):
    return [Item(w, v) for w, v in pairs]


print(sol.optimum_subject_to_capacity(as_items([(5, 60), (3, 50), (4, 70), (2, 30)]), 5))  # 80

# four = as_items([(5, 60), (3, 50), (4, 70), (2, 30)])
# assert sol.optimum_subject_to_capacity(four, 5) == 80
# assert sol.optimum_subject_to_capacity(four, 9) == 150
# assert sol.optimum_subject_to_capacity(as_items([(3, 7)]), 2) == 0
# assert sol.optimum_subject_to_capacity(as_items([(3, 7)]), 3) == 7
# assert sol.optimum_subject_to_capacity(four, 0) == 0
# assert sol.optimum_subject_to_capacity(four, 14) == 210
# assert sol.optimum_subject_to_capacity(four, 1000) == 210
# assert sol.optimum_subject_to_capacity(as_items([(1, 1), (1, 1), (1, 1)]), 2) == 2
# assert sol.optimum_subject_to_capacity(as_items([(6, 30), (3, 14), (4, 16), (2, 9)]), 10) == 46
# assert sol.optimum_subject_to_capacity(as_items([(1000, 1000)]), 1000) == 1000
# assert sol.optimum_subject_to_capacity(as_items([(1000, 1000)]), 999) == 0
# assert sol.optimum_subject_to_capacity([Item(10, 10)] * 100, 995) == 990
# big = [Item(w, (i * 37) % 101 + 1) for i, w in enumerate(range(1, 101))]
# assert sol.optimum_subject_to_capacity(big, 100) == 743
# assert sol.optimum_subject_to_capacity(big, 1000) == 2559
