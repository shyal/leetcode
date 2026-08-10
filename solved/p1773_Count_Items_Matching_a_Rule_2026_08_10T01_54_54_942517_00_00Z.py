"""
URL: https://leetcode.com/problems/count-items-matching-a-rule/description/?envType=problem-list-v2&envId=vn57k9wr

1773. Count Items Matching a Rule

You are given an array items, where each items[i] = [type_i, color_i, name_i]
describes the type, color, and name of the i-th item. You are also given a rule
represented by two strings, ruleKey and ruleValue.

The i-th item is said to match the rule if one of the following is true:

    - ruleKey == "type" and ruleValue == type_i.
    - ruleKey == "color" and ruleValue == color_i.
    - ruleKey == "name" and ruleValue == name_i.

Return the number of items that match the given rule.


Example 1:

Input: items = [["phone","blue","pixel"],["computer","silver","lenovo"],["phone","gold","iphone"]], ruleKey = "color", ruleValue = "silver"
Output: 1
Explanation: There is only one item matching the given rule, which is ["computer","silver","lenovo"].

Example 2:

Input: items = [["phone","blue","pixel"],["computer","silver","phone"],["phone","gold","iphone"]], ruleKey = "type", ruleValue = "phone"
Output: 2
Explanation: There are only two items matching the given rule, which are ["phone","blue","pixel"] and ["phone","gold","iphone"]. Note that the item ["computer","silver","phone"] does not match.


Constraints:

    1 <= items.length <= 10^4
    1 <= type_i.length, color_i.length, name_i.length, ruleValue.length <= 10
    ruleKey is equal to either "type", "color", or "name".
    All strings consist only of lowercase letters.
"""


class Solution:
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        ruleIndices = {
            "type": 0,
            "color": 1,
            "name": 2
        }
        return sum(item[ruleIndices[ruleKey]] == ruleValue for item in items)


sol = Solution()

print(
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]],
        "color",
        "silver",
    )
)  # 1

assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]],
        "color",
        "silver",
    )
    == 1
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "phone"], ["phone", "gold", "iphone"]],
        "type",
        "phone",
    )
    == 2
)

assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "phone"], ["phone", "gold", "iphone"]],
        "name",
        "phone",
    )
    == 1
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]],
        "name",
        "pixel",
    )
    == 1
)

assert sol.countMatches([["phone", "blue", "pixel"]], "type", "phone") == 1
assert sol.countMatches([["phone", "blue", "pixel"]], "color", "blue") == 1
assert sol.countMatches([["phone", "blue", "pixel"]], "name", "pixel") == 1
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "blue") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "pixel") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "color", "phone") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "color", "pixel") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "name", "phone") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "name", "blue") == 0

assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"]], "color", "gold"
    )
    == 0
)

assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["phone", "blue", "pixel"], ["phone", "blue", "pixel"]],
        "color",
        "blue",
    )
    == 3
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["phone", "blue", "pixel"], ["phone", "blue", "pixel"]],
        "type",
        "phone",
    )
    == 3
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["phone", "blue", "pixel"], ["phone", "blue", "pixel"]],
        "name",
        "pixel",
    )
    == 3
)

assert sol.countMatches([["silver", "silver", "silver"]], "type", "silver") == 1
assert sol.countMatches([["silver", "silver", "silver"]], "color", "silver") == 1
assert sol.countMatches([["silver", "silver", "silver"]], "name", "silver") == 1

assert (
    sol.countMatches(
        [["a", "b", "c"], ["b", "c", "a"], ["c", "a", "b"]],
        "type",
        "a",
    )
    == 1
)
assert (
    sol.countMatches(
        [["a", "b", "c"], ["b", "c", "a"], ["c", "a", "b"]],
        "color",
        "a",
    )
    == 1
)
assert (
    sol.countMatches(
        [["a", "b", "c"], ["b", "c", "a"], ["c", "a", "b"]],
        "name",
        "a",
    )
    == 1
)
assert (
    sol.countMatches(
        [["a", "b", "c"], ["b", "c", "a"], ["c", "a", "b"]],
        "name",
        "d",
    )
    == 0
)

assert (
    sol.countMatches(
        [["abcdefghij", "klmnopqrst", "uvwxyzabcd"], ["abcdefghi", "klmnopqrst", "uvwxyzabcd"]],
        "type",
        "abcdefghij",
    )
    == 1
)
assert (
    sol.countMatches(
        [["abcdefghij", "klmnopqrst", "uvwxyzabcd"], ["abcdefghi", "klmnopqrst", "uvwxyzabcd"]],
        "color",
        "klmnopqrst",
    )
    == 2
)

assert sol.countMatches([["phone", "blue", "pixel"] for _ in range(10000)], "type", "phone") == 10000
assert sol.countMatches([["phone", "blue", "pixel"] for _ in range(10000)], "name", "lenovo") == 0
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"] if i % 2 == 0 else ["laptop", "gold", "mac"] for i in range(10000)],
        "color",
        "gold",
    )
    == 5000
)