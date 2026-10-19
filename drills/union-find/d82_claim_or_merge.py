"""
DRILL: Claim Or Merge

Given a list of accounts, where accounts[i] is a list of email addresses
belonging to account i, group accounts that share emails using Union-Find.

Return a dictionary mapping each unique email to the index of the first
account that listed it.

An email is claimed by the first account that lists it. When a later
account lists an email that has already been claimed, merge the two
accounts using Union-Find.

Two accounts can end up in the same group even if they don't share an
email directly, as long as they are connected through other accounts.

Example 1:

Input: accounts = [["js@m.co", "jn@m.co"], ["mary@m.co"], ["jn@m.co", "j0@m.co"], ["m2@m.co", "mary@m.co"]]
Output: {"js@m.co": 0, "jn@m.co": 0, "mary@m.co": 1, "j0@m.co": 2, "m2@m.co": 3}
Explanation:

    - Account 0 claims js@m.co and jn@m.co.
    - Account 1 claims mary@m.co.
    - Account 2 lists jn@m.co, which account 0 already claimed.
      Merge accounts 2 and 0 using union(2, 0).
    - Account 3 lists mary@m.co, which account 1 already claimed.
      Merge accounts 3 and 1 using union(3, 1).

Example 2:

Input: accounts = [["g@m.co"], ["g@m.co"], ["g@m.co"]]
Output: {"g@m.co": 0}
Explanation:

    - Account 0 claims g@m.co.
    - Account 1 lists the same email, so call union(1, 0).
    - Account 2 lists the same email, so call union(2, 0).

Constraints:

    1 <= len(accounts) <= 1000
    1 <= len(accounts[i]) <= 10

Requirements:

    - Perform exactly one dictionary lookup per email.
    - Call union at most once per email.
    - Do not compare account pairs directly.
    - Do not make a second pass over the accounts.

The solution extends UnionFind from dsa/union_find.py.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def union_shared(self, accounts: List[List[str]]) -> Dict[str, int]:
        pass


sol = Solution(4)

print(sol.union_shared([["js@m.co", "jn@m.co"], ["mary@m.co"], ["jn@m.co", "j0@m.co"], ["m2@m.co", "mary@m.co"]]))
# {'js@m.co': 0, 'jn@m.co': 0, 'mary@m.co': 1, 'j0@m.co': 2, 'm2@m.co': 3}
print(sol.find(2), sol.find(3))  # 0 1

# sol = Solution(4)
# assert sol.union_shared([["js@m.co", "jn@m.co"], ["mary@m.co"], ["jn@m.co", "j0@m.co"], ["m2@m.co", "mary@m.co"]]) == {"js@m.co": 0, "jn@m.co": 0, "mary@m.co": 1, "j0@m.co": 2, "m2@m.co": 3}
# assert sol.find(2) == 0
# assert sol.find(3) == 1

# sol = Solution(3)
# assert sol.union_shared([["g@m.co"], ["g@m.co"], ["g@m.co"]]) == {"g@m.co": 0}
# assert sol.find(1) == 0
# assert sol.find(2) == 0

# sol = Solution(1)
# assert sol.union_shared([["e@m.co"]]) == {"e@m.co": 0}

# sol = Solution(2)
# assert sol.union_shared([["a@m.co", "b@m.co"], ["c@m.co", "d@m.co"]]) == {"a@m.co": 0, "b@m.co": 0, "c@m.co": 1, "d@m.co": 1}
# assert sol.find(0) == 0
# assert sol.find(1) == 1

# sol = Solution(5)
# assert sol.union_shared([["a@m.co"], ["b@m.co", "a@m.co"], ["c@m.co"], ["d@m.co", "c@m.co"], ["d@m.co"]]) == {"a@m.co": 0, "b@m.co": 1, "c@m.co": 2, "d@m.co": 3}
# assert sol.find(1) == 0
# assert sol.find(3) == 2
# assert sol.find(4) == 2
