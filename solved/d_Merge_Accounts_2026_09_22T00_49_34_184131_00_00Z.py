"""
DRILL: Merge Accounts

There are email accounts, out in the world. A person may own multiple
email accounts. An account can have multiple email IDs.

Person
   |
   ---> Account1
           |
           ---> email ID1
           ---> email ID1
   ---> Account2
           |
           ---> email ID1
           ---> email ID1


Union find lets's us discover who these emails belong to. Which person
they belong to, even though `person` is never given to you.

Bear in mind that `person` also doesn't exist. It's simply a placeholder
for the `account` that really owns the email. We actually just want
to merge the accounts.

Start by creating the persons dictionary.

Then enumerate over the accounts, to make `account` and `emails` available.

Then, to find the enigmatic `person`: call find on the account. This is because
some merges were already created in the assert lines.

What we're really interested in knowing is, which person owns which email.


Example 1:

Input: accounts = [["js@m.co", "jn@m.co"], ["mary@m.co"], ["jn@m.co", "j0@m.co"], ["m2@m.co", "mary@m.co"]]
Output: {0: {"js@m.co", "jn@m.co", "j0@m.co"}, 1: {"mary@m.co", "m2@m.co"}}
Explanation: i is an account. find(i) is the person who owns it. One
person can own several accounts, so accounts 0 and 2 both map to person
0, and accounts 1 and 3 both map to person 1.

          person 0                        person 1
        +------------+                  +------------+
        | account 0  |                  | account 1  |
        | js@m.co    |                  | mary@m.co  |
        | jn@m.co    |                  +------------+
        +------------+                        ^
              ^                               | find(3) = 1
              | find(2) = 0             +------------+
        +------------+                  | account 3  |
        | account 2  |                  | m2@m.co    |
        | jn@m.co    |                  | mary@m.co  |
        | j0@m.co    |                  +------------+
        +------------+

    person 0: {js@m.co, jn@m.co, j0@m.co}
    person 1: {mary@m.co, m2@m.co}

Example 2:

Input: accounts = [["g@m.co"], ["g@m.co"], ["g@m.co"]]
Output: {0: {"g@m.co"}}
Explanation: 1 -> 0 and 2 -> 0, so all three accounts have root 0.

Constraints:

    1 <= len(accounts) <= 1000
    1 <= len(accounts[i]) <= 10

    REQUIRED: must call self.find at most once per account. NO
    account-to-account pair tests; NO scan for roots other than through
    self.find.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def mergeAccounts(self, accounts: List[List[str]]) -> Dict[int, set]:
        persons = defaultdict(set)
        for account, emails in enumerate(accounts):
            root = self.find(account)
            for email in emails:
                persons[root].add(email)
        return persons


sol = Solution(4)

accounts = [
    ["js@m.co", "jn@m.co"],
    ["mary@m.co"],
    ["jn@m.co", "j0@m.co"],
    ["m2@m.co", "mary@m.co"],
]
sol.union_shared(accounts)
print(sol.mergeAccounts(accounts))
# {0: {'js@m.co', 'jn@m.co', 'j0@m.co'}, 1: {'mary@m.co', 'm2@m.co'}}

accounts = [
    ["js@m.co", "jn@m.co"],
    ["mary@m.co"],
    ["jn@m.co", "j0@m.co"],
    ["m2@m.co", "mary@m.co"],
]
sol = Solution(4)
sol.union_shared(accounts)
assert sol.mergeAccounts(accounts) == {
    0: {"js@m.co", "jn@m.co", "j0@m.co"},
    1: {"mary@m.co", "m2@m.co"},
}

accounts = [["g@m.co"], ["g@m.co"], ["g@m.co"]]
sol = Solution(3)
sol.union_shared(accounts)
assert sol.mergeAccounts(accounts) == {0: {"g@m.co"}}

accounts = [["e@m.co"]]
sol = Solution(1)
sol.union_shared(accounts)
assert sol.mergeAccounts(accounts) == {0: {"e@m.co"}}

accounts = [["a@m.co", "b@m.co"], ["c@m.co", "d@m.co"]]
sol = Solution(2)
sol.union_shared(accounts)
assert sol.mergeAccounts(accounts) == {0: {"a@m.co", "b@m.co"}, 1: {"c@m.co", "d@m.co"}}

accounts = [
    ["a@m.co"],
    ["b@m.co", "a@m.co"],
    ["c@m.co"],
    ["d@m.co", "c@m.co"],
    ["d@m.co"],
]
sol = Solution(5)
sol.union_shared(accounts)
assert sol.mergeAccounts(accounts) == {0: {"a@m.co", "b@m.co"}, 2: {"c@m.co", "d@m.co"}}
