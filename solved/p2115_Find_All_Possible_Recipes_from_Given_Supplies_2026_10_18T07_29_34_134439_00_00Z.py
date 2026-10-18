"""
URL: https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/description/?envType=problem-list-v2&envId=vn57k9wr

2115. Find All Possible Recipes from Given Supplies

You have information about n different recipes. You are given a string array recipes and a 2D string array ingredients. The i-th recipe has the name recipes[i], and you can create it if you have all the needed ingredients from ingredients[i]. A recipe can also be an ingredient for other recipes, i.e., ingredients[i] may contain a string that is in recipes.

You are also given a string array supplies containing all the ingredients that you initially have, and you have an infinite supply of all of them.

Return a list of all the recipes that you can create. You may return the answer in any order.

Note that two recipes may contain each other in their ingredients.

Example 1:

Input: recipes = ["bread"], ingredients = [["yeast","flour"]], supplies = ["yeast","flour","corn"]
Output: ["bread"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".

Example 2:

Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".

Example 3:

Input: recipes = ["bread","sandwich","burger"], ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich","burger"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
We can create "burger" since we have the ingredient "meat" and can create the ingredients "bread" and "sandwich".

Constraints:

    n == recipes.length == ingredients.length
    1 <= n <= 100
    1 <= ingredients[i].length, supplies.length <= 100
    1 <= recipes[i].length, ingredients[i][j].length, supplies[k].length <= 10
    recipes[i], ingredients[i][j], and supplies[k] consist only of lowercase English letters.
    All the values of recipes and supplies combined are unique.
    Each ingredients[i] does not contain any duplicate values.
"""


class Solution:
    def findAllRecipes(
        self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]
    ) -> List[str]:
        pass


sol = Solution()

# Example 1
# print(
    sol.findAllRecipes(["bread"], [["yeast", "flour"]], ["yeast", "flour", "corn"])
)  # ["bread"]

# assert uses(Solution, adjacency, indegrees)
# assert sorted(
#     sol.findAllRecipes(["bread"], [["yeast", "flour"]], ["yeast", "flour", "corn"])
# ) == sorted(["bread"])
# assert sorted(
#     sol.findAllRecipes(
#         ["bread", "sandwich"],
#         [["yeast", "flour"], ["bread", "meat"]],
#         ["yeast", "flour", "meat"],
#     )
# ) == sorted(["bread", "sandwich"])
# assert sorted(
#     sol.findAllRecipes(
#         ["bread", "sandwich", "burger"],
#         [["yeast", "flour"], ["bread", "meat"], ["sandwich", "meat", "bread"]],
#         ["yeast", "flour", "meat"],
#     )
# ) == sorted(["bread", "sandwich", "burger"])

# assert sorted(sol.findAllRecipes(["a"], [["b"]], ["c"])) == []
# assert sorted(sol.findAllRecipes(["self"], [["self"]], [])) == []
# assert sorted(sol.findAllRecipes(["a", "b"], [["b"], ["a"]], [])) == []
# assert sorted(
#     sol.findAllRecipes(["r1", "r2", "r3"], [["ing"], ["r1"], ["r2"]], ["ing"])
# ) == ["r1", "r2", "r3"]
# assert sorted(
#     sol.findAllRecipes(
#         ["cake", "frosting", "icing"],
#         [["flour", "sugar"], ["sugar", "butter"], ["butter"]],
#         ["flour", "sugar", "butter"],
#     )
# ) == ["cake", "frosting", "icing"]
# assert sorted(
#     sol.findAllRecipes(
#         ["salad", "dressing"],
#         [["lettuce", "tomato"], ["oil", "salt"]],
#         ["lettuce", "tomato"],
#     )
# ) == ["salad"]
# assert sorted(
#     sol.findAllRecipes(
#         [f"r{i}" for i in range(40)],
#         [[f"r{i-1}"] if i > 0 else ["seed"] for i in range(40)],
#         ["seed"],
#     )
# ) == [
#     "r0",
#     "r1",
#     "r10",
#     "r11",
#     "r12",
#     "r13",
#     "r14",
#     "r15",
#     "r16",
#     "r17",
#     "r18",
#     "r19",
#     "r2",
#     "r20",
#     "r21",
#     "r22",
#     "r23",
#     "r24",
#     "r25",
#     "r26",
#     "r27",
#     "r28",
#     "r29",
#     "r3",
#     "r30",
#     "r31",
#     "r32",
#     "r33",
#     "r34",
#     "r35",
#     "r36",
#     "r37",
#     "r38",
#     "r39",
#     "r4",
#     "r5",
#     "r6",
#     "r7",
#     "r8",
#     "r9",
# ]
# assert sorted(
#     sol.findAllRecipes(["a", "b", "c"], [["x"], ["x"], ["a", "b"]], ["x"])
# ) == ["a", "b", "c"]
