"""
URL: https://leetcode.com/problems/minimum-index-sum-of-two-lists/description/?envType=problem-list-v2&envId=vn57k9wr

599. Minimum Index Sum of Two Lists

Given two arrays of strings list1 and list2, find the common strings with the least index sum.

A common string is a string that appeared in both list1 and list2.

A common string with the least index sum is a common string such that if it appeared at list1[i] and list2[j] then i + j should be the minimum value among all the other common strings.

Return all the common strings with the least index sum. Return the answer in any order.

Example 1:

Input: list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]
Output: ["Shogun"]
Explanation: The only common string is "Shogun".

Example 2:

Input: list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["KFC","Shogun","Burger King"]
Output: ["Shogun"]
Explanation: The common string with the least index sum is "Shogun" with index sum = (0 + 1) = 1.

Example 3:

Input: list1 = ["happy","sad","good"], list2 = ["sad","happy","good"]
Output: ["sad","happy"]
Explanation: There are three common strings:
"happy" with index sum = (0 + 1) = 1.
"sad" with index sum = (1 + 0) = 1.
"good" with index sum = (2 + 2) = 4.
The strings with the least index sum are "sad" and "happy".

Constraints:

    1 <= list1.length, list2.length <= 1000
    1 <= list1[i].length, list2[i].length <= 30
    list1[i] and list2[i] consist of spaces ' ' and English letters.
    All the strings of list1 are unique.
    All the strings of list2 are unique.
    There is at least a common string between list1 and list2.
"""


class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        D = {v: i for i, v in enumerate(list2)}
        common = defaultdict(list)
        for i, r in enumerate(list1):
            if r in D:
                common[i + D[r]].append(r)
        return common[min(common.keys())]


sol = Solution()

# print(
#     sol.findRestaurant(
#         ["Shogun", "Tapioca Express", "Burger King", "KFC"],
#         ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"],
#     )
# )  # ["Shogun"]

assert sorted(
    sol.findRestaurant(
        ["Shogun", "Tapioca Express", "Burger King", "KFC"],
        ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"],
    )
) == sorted(["Shogun"])
assert sorted(
    sol.findRestaurant(
        ["Shogun", "Tapioca Express", "Burger King", "KFC"],
        ["KFC", "Shogun", "Burger King"],
    )
) == sorted(["Shogun"])
assert sorted(
    sol.findRestaurant(["happy", "sad", "good"], ["sad", "happy", "good"])
) == sorted(["sad", "happy"])
assert sorted(sol.findRestaurant(["A"], ["A"])) == sorted(["A"])
assert sorted(sol.findRestaurant(["A", "B"], ["A", "C"])) == sorted(["A"])
assert sorted(sol.findRestaurant(["A", "B", "C"], ["B", "A", "D"])) == sorted(
    ["A", "B"]
)
assert sorted(sol.findRestaurant(["A", "B"], ["B", "A"])) == sorted(["A", "B"])
assert sorted(
    sol.findRestaurant(["X", "Y", "Z", "Common"], ["P", "Q", "Common"])
) == sorted(["Common"])
assert sorted(
    sol.findRestaurant(["Common1", "Common2"], ["Common1", "X", "Y", "Common2"])
) == sorted(["Common1"])
assert sorted(
    sol.findRestaurant(["Happy Meal", "Big Mac"], ["Big Mac", "Happy Meal"])
) == sorted(["Big Mac", "Happy Meal"])
assert sorted(sol.findRestaurant([" ", "A "], [" ", "B"])) == sorted([" "])
assert sorted(sol.findRestaurant(["Z", "Y", "X"], ["X", "Y", "Z"])) == sorted(
    ["Z", "Y", "X"]
)
assert sorted(sol.findRestaurant(["A", "B", "C", "D"], ["D", "C", "B", "A"])) == sorted(
    ["A", "B", "C", "D"]
)
