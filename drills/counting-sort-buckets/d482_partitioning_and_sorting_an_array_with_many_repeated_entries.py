"""
EPI 13.9 Partitioning and sorting an array with many repeated entries

Given a list people of pairs (age, name), reorder it in place so that
all the people with the same age are next to each other. The groups can
be in any order, and the order inside a group does not matter.

Example 1:

Input: people = [(30, "Ana"), (25, "Ben"), (30, "Cy"), (40, "Dee"), (25, "Eve")]
Output: people becomes [(30, "Ana"), (30, "Cy"), (25, "Ben"), (25, "Eve"), (40, "Dee")]
Explanation: any order with the two 30s together and the two 25s
together is also correct.

Example 2:

Input: people = [(7, "Al"), (7, "Bo")]
Output: people stays the same, or becomes [(7, "Bo"), (7, "Al")]

Example 3:

Input: people = []
Output: people stays []

Constraints:

    0 <= len(people) <= 10^5
    0 <= age <= 10^9
    Names are nonempty strings of letters or digits.

    REQUIRED: O(n) time, where n is the length of people, and O(m) extra
    space, where m is the number of distinct ages. NO sorting.
"""


class Solution:
    def group_by_age(self, people: list[tuple[int, str]]) -> None:
        pass


sol = Solution()

people = [(30, "Ana"), (25, "Ben"), (30, "Cy"), (40, "Dee"), (25, "Eve")]
sol.group_by_age(people)
print(people)  # [(30, "Ana"), (30, "Cy"), (25, "Ben"), (25, "Eve"), (40, "Dee")]

# people = [(30, "Ana"), (25, "Ben"), (30, "Cy"), (40, "Dee"), (25, "Eve")]
# sol.group_by_age(people)
# assert sorted(people) == [(25, "Ben"), (25, "Eve"), (30, "Ana"), (30, "Cy"), (40, "Dee")]
# assert len(list(groupby(a for a, _ in people))) == 3
# people = [(7, "Al"), (7, "Bo")]
# sol.group_by_age(people)
# assert sorted(people) == [(7, "Al"), (7, "Bo")]
# people = []
# sol.group_by_age(people)
# assert people == []
# people = [(1, "x")]
# sol.group_by_age(people)
# assert people == [(1, "x")]
# people = [(1, "a"), (2, "b"), (1, "c")]
# sol.group_by_age(people)
# assert sorted(people) == [(1, "a"), (1, "c"), (2, "b")]
# assert len(list(groupby(a for a, _ in people))) == 2
# people = [(1, "a"), (2, "b"), (3, "c"), (1, "d"), (2, "e"), (3, "f")]
# sol.group_by_age(people)
# assert sorted(people) == [(1, "a"), (1, "d"), (2, "b"), (2, "e"), (3, "c"), (3, "f")]
# assert len(list(groupby(a for a, _ in people))) == 3
# people = [(5, "p"), (5, "q"), (5, "q"), (6, "r")]
# sol.group_by_age(people)
# assert sorted(people) == [(5, "p"), (5, "q"), (5, "q"), (6, "r")]
# assert len(list(groupby(a for a, _ in people))) == 2
# people = [(i % 100, str(i)) for i in range(10 ** 5)]
# before = Counter(people)
# sol.group_by_age(people)
# assert Counter(people) == before
# assert len(list(groupby(a for a, _ in people))) == 100
# people = [(10 ** 9 - i % 2, str(i)) for i in range(10 ** 5)]
# sol.group_by_age(people)
# assert len(list(groupby(a for a, _ in people))) == 2 and len(people) == 10 ** 5
# people = [(i, str(i)) for i in range(10 ** 5)]
# sol.group_by_age(people)
# assert sorted(people) == [(i, str(i)) for i in range(10 ** 5)]
