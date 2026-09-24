# REFERENCE: d83 Merge Accounts
from dsa.union_find import UnionFind
extends UnionFind

def mergeAccounts(accounts: [[str]]) -> {int: {str}}
  persons = defaultdict(set)
  for account, emails in accounts
    person = self.find(account)  # find on the account, not the email
    for email in emails
      persons[person].add(email)
  persons
