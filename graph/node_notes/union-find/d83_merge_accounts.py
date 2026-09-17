# REFERENCE: d83 Merge Accounts
class Solution(UnionFind):
    def mergeAccounts(self, accounts):
        persons = defaultdict(set)
        for account, emails in enumerate(accounts):
            person = self.find(account)  # find on the account, not the email
            for email in emails:
                persons[person].add(email)
        return persons
