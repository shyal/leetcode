# REFERENCE: d482 EPI 13.9 Partitioning and sorting an array with many repeated entries
class Solution:
    def group_by_age(self, people):
        counts = Counter(age for age, _ in people)
        nxt, end, total = {}, {}, 0
        for age, c in counts.items():
            nxt[age], total = total, total + c
            end[age] = total
        for age in counts:
            while nxt[age] < end[age]:
                other = people[nxt[age]][0]
                if other == age:
                    nxt[age] += 1
                else:
                    i, j = nxt[age], nxt[other]
                    people[i], people[j] = people[j], people[i]
                    nxt[other] += 1
