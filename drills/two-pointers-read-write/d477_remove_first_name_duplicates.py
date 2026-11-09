"""
EPI 13.4 Remove first-name duplicates

Given a list A of names, each a pair (first_name, last_name), remove
entries in place so that each first name appears exactly once. Any
entry with a given first name may be the entry that stays, and the
order of A after the call does not matter.

Example 1:

Input: A = [("Ana", "Cruz"), ("Ben", "Ito"), ("Ana", "Lee"), ("Ana", "Diaz")]
Output: A becomes [("Ana", "Cruz"), ("Ben", "Ito")]
Explanation: ("Ana", "Lee") or ("Ana", "Diaz") in place of
("Ana", "Cruz") is also correct, in any order.

Example 2:

Input: A = [("Ben", "Ito"), ("Cy", "Ito")]
Output: A stays the same, in any order
Explanation: the last names are equal, but the first names are not.

Example 3:

Input: A = []
Output: A stays []

Constraints:

    0 <= len(A) <= 10^5
    Each name is a nonempty string of letters.

    REQUIRED: O(n log n) time, where n is the length of A, and O(1)
    extra space beyond the sort. NO set or dict. NO new list.
"""


class Solution:
    def eliminate_duplicate(self, A: list[tuple[str, str]]) -> None:
        pass


sol = Solution()

A = [("Ana", "Cruz"), ("Ben", "Ito"), ("Ana", "Lee"), ("Ana", "Diaz")]
sol.eliminate_duplicate(A)
print(A)  # [("Ana", "Cruz"), ("Ben", "Ito")]

# A = [("Ana", "Cruz"), ("Ben", "Ito"), ("Ana", "Lee"), ("Ana", "Diaz")]
# sol.eliminate_duplicate(A)
# assert sorted(f for f, _ in A) == ["Ana", "Ben"] and ("Ben", "Ito") in A
# assert set(A) <= {("Ana", "Cruz"), ("Ben", "Ito"), ("Ana", "Lee"), ("Ana", "Diaz")}
# A = [("Ben", "Ito"), ("Cy", "Ito")]
# sol.eliminate_duplicate(A)
# assert sorted(A) == [("Ben", "Ito"), ("Cy", "Ito")]
# A = []
# sol.eliminate_duplicate(A)
# assert A == []
# A = [("Dee", "Ross")]
# sol.eliminate_duplicate(A)
# assert A == [("Dee", "Ross")]
# A = [("Dee", "Ross"), ("Dee", "Ross")]
# sol.eliminate_duplicate(A)
# assert A == [("Dee", "Ross")]
# A = [("Eve", "Hart"), ("Eve", "Kim")]
# sol.eliminate_duplicate(A)
# assert A in [[("Eve", "Hart")], [("Eve", "Kim")]]
# A = [("Cy", "Bo"), ("Ana", "Bo"), ("Ben", "Bo"), ("Ana", "Al"), ("Cy", "Al"), ("Ben", "Al")]
# sol.eliminate_duplicate(A)
# assert sorted(f for f, _ in A) == ["Ana", "Ben", "Cy"]
# assert set(A) <= {("Cy", "Bo"), ("Ana", "Bo"), ("Ben", "Bo"), ("Ana", "Al"), ("Cy", "Al"), ("Ben", "Al")}
# A = [("ana", "X"), ("Ana", "X")]
# sol.eliminate_duplicate(A)
# assert sorted(A) == [("Ana", "X"), ("ana", "X")]
# A = [(f"n{i % 1000}", f"m{i}") for i in range(10 ** 5)]
# sol.eliminate_duplicate(A)
# assert sorted(f for f, _ in A) == sorted(f"n{i}" for i in range(1000))
# assert all(int(l[1:]) % 1000 == int(f[1:]) for f, l in A)
# A = [(f"n{i}", "x") for i in range(10 ** 5)]
# sol.eliminate_duplicate(A)
# assert len(A) == 10 ** 5
