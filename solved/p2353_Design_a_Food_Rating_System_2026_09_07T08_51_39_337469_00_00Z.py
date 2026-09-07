"""
URL: https://leetcode.com/problems/design-a-food-rating-system/description/?envType=problem-list-v2&envId=vn57k9wr

2353. Design a Food Rating System

Design a food rating system that can do the following:

- Modify the rating of a food item listed in the system.
- Return the highest-rated food item for a type of cuisine in the system.

Implement the FoodRatings class:

- FoodRatings(String[] foods, String[] cuisines, int[] ratings) Initializes the system. The food items are described by foods, cuisines and ratings, all of which have a length of n.
  - foods[i] is the name of the iᵗʰ food,
  - cuisines[i] is the type of cuisine of the iᵗʰ food, and
  - ratings[i] is the initial rating of the iᵗʰ food.
- void changeRating(String food, int newRating) Changes the rating of the food item with the name food.
- String highestRated(String cuisine) Returns the name of the food item that has the highest rating for the given type of cuisine. If there is a tie, return the item with the lexicographically smaller name.

Note that a string x is lexicographically smaller than string y if x comes before y in dictionary order, that is, either x is a prefix of y, or if i is the first position such that x[i] != y[i], then x[i] comes before y[i] in alphabetic order.

Example 1:

Input
["FoodRatings","highestRated","highestRated","changeRating","highestRated","changeRating","highestRated"]
[[["kimchi","miso","sushi","moussaka","ramen","bulgogi"],["korean","japanese","japanese","greek","japanese","korean"],[9,12,8,15,14,7]],["korean"],["japanese"],["sushi",16],["japanese"],["ramen",16],["japanese"]]
Output
[null,"kimchi","ramen",null,"sushi",null,"ramen"]

Explanation
FoodRatings foodRatings = new FoodRatings(["kimchi","miso","sushi","moussaka","ramen","bulgogi"], ["korean","japanese","japanese","greek","japanese","korean"], [9,12,8,15,14,7]);
foodRatings.highestRated("korean"); // return "kimchi"
                                   // "kimchi" is the highest rated korean food with a rating of 9.
foodRatings.highestRated("japanese"); // return "ramen"
                                     // "ramen" is the highest rated japanese food with a rating of 14.
foodRatings.changeRating("sushi", 16); // "sushi" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "sushi"
                                     // "sushi" is the highest rated japanese food with a rating of 16.
foodRatings.changeRating("ramen", 16); // "ramen" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "ramen"
                                     // Both "sushi" and "ramen" have a rating of 16.
                                     // However, "ramen" is lexicographically smaller than "sushi".

Constraints:

    1 <= n <= 2 * 10^4
    n == foods.length == cuisines.length == ratings.length
    1 <= foods[i].length, cuisines[i].length <= 10
    foods[i], cuisines[i] consist of lowercase English letters.
    1 <= ratings[i] <= 10^8
    All the strings in foods are distinct.
    food will be the name of a food item in the system across all calls to changeRating.
    cuisine will be a type of cuisine of at least one food item in the system across all calls to highestRated.
    At most 2 * 10^4 calls in total will be made to changeRating and highestRated.
"""


class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.ratings = defaultdict(list)
        self.updates = {}
        self.food_cuisines = {}
        for food, cuisine, rating in zip(foods, cuisines, ratings):
            heappush(self.ratings[cuisine], (-rating, food))
            self.food_cuisines[food] = cuisine

    def changeRating(self, food: str, newRating: int) -> None:
        self.updates[food] = newRating
        heappush(self.ratings[self.food_cuisines[food]], (-newRating, food))

    def highestRated(self, cuisine: str) -> str:
        while True:
            rating, food = self.ratings[cuisine][0]
            if food in self.updates:
                if self.updates[food] == -rating:
                    return food
                else:
                    heappop(self.ratings[cuisine])
                    continue
            return food


sol = FoodRatings(
    ["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
    ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
    [9, 12, 8, 15, 14, 7],
)

print(sol.highestRated("korean"))  # "kimchi"

assert sol.highestRated("korean") == "kimchi"
assert sol.highestRated("japanese") == "ramen"
sol.changeRating("sushi", 16)
assert sol.highestRated("japanese") == "sushi"
sol.changeRating("ramen", 16)
assert sol.highestRated("japanese") == "ramen"

assert FoodRatings(["a"], ["cuisine"], [1]).highestRated("cuisine") == "a"


# edge cases: one line each, the values are the reference solution's.
assert [(fr := FoodRatings(["a"], ["z"], [1])), fr.highestRated("z")][
    -1
] == "a"  # single_food_single_cuisine
assert [
    (fr := FoodRatings(["a"], ["z"], [1])),
    fr.changeRating("a", 100000000),
    fr.highestRated("z"),
][
    -1
] == "a"  # only_food_rating_raised_to_maximum
assert [
    (fr := FoodRatings(["a"], ["z"], [5])),
    fr.changeRating("a", 5),
    fr.highestRated("z"),
][
    -1
] == "a"  # rating_changed_to_the_same_value
assert [(fr := FoodRatings(["b", "a"], ["z", "z"], [7, 7])), fr.highestRated("z")][
    -1
] == "a"  # two_foods_tie_on_initial_rating
assert [
    (fr := FoodRatings(["a", "b"], ["z", "z"], [9, 3])),
    fr.changeRating("a", 1),
    fr.highestRated("z"),
][
    -1
] == "b"  # leader_lowered_below_the_other_food
assert [
    (fr := FoodRatings(["a", "b"], ["z", "z"], [9, 3])),
    fr.changeRating("b", 9),
    fr.highestRated("z"),
][
    -1
] == "a"  # trailing_food_raised_into_a_tie
assert [(fr := FoodRatings(["ab", "abc"], ["z", "z"], [4, 4])), fr.highestRated("z")][
    -1
] == "ab"  # tie_between_a_name_and_its_prefix
assert [
    (fr := FoodRatings(["a", "b"], ["y", "z"], [1, 100000000])),
    fr.highestRated("y"),
][
    -1
] == "a"  # cuisine_queried_holds_only_the_lower_rated_food
assert [
    (fr := FoodRatings(["a", "b", "c"], ["z", "z", "z"], [1, 2, 3])),
    fr.changeRating("c", 1),
    fr.changeRating("b", 1),
    fr.highestRated("z"),
][
    -1
] == "a"  # every_food_in_a_cuisine_lowered_to_a_tie
assert [
    (fr := FoodRatings(["a", "b"], ["z", "z"], [1, 2])),
    fr.changeRating("a", 5),
    fr.changeRating("a", 3),
    fr.changeRating("a", 1),
    fr.highestRated("z"),
][
    -1
] == "b"  # one_food_rated_repeatedly_up_then_down
assert [
    (fr := FoodRatings(["p", "q", "r"], ["z", "z", "y"], [3, 5, 8])),
    fr.changeRating("r", 1),
    fr.changeRating("q", 2),
    fr.highestRated("z"),
    fr.highestRated("y"),
][
    -2
] == "p"  # changes_interleaved_across_two_cuisines
assert [
    (fr := FoodRatings(["a", "b", "c"], ["z", "z", "z"], [100000000, 1, 1])),
    fr.changeRating("a", 1),
    fr.changeRating("b", 100000000),
    fr.highestRated("z"),
][
    -1
] == "b"  # extreme_ratings_swapped_between_two_foods
