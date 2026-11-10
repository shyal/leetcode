# URL: https://leetcode.com/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1452. People Whose List of Favorite Companies Is Not a Subset of Another List
#
# Given the array favoriteCompanies where favoriteCompanies[i] is the list of favorites companies for the ith person (indexed from 0).
#
# Return the indices of people whose list of favorite companies is not a subset of any other list of favorites companies. You must return the indices in increasing order.
#
# Example 1:
#
# Input: favoriteCompanies = [["leetcode","google","facebook"],["google","microsoft"],["google","facebook"],["google"],["amazon"]]
# Output: [0,1,4]
# Explanation:
# Person with index=2 has favoriteCompanies[2]=["google","facebook"] which is a subset of favoriteCompanies[0]=["leetcode","google","facebook"] corresponding to the person with index 0.
# Person with index=3 has favoriteCompanies[3]=["google"] which is a subset of favoriteCompanies[0]=["leetcode","google","facebook"] and favoriteCompanies[1]=["google","microsoft"].
# Other lists of favorite companies are not a subset of another list, therefore, the answer is [0,1,4].
#
# Example 2:
#
# Input: favoriteCompanies = [["leetcode","google","facebook"],["leetcode","amazon"],["facebook","google"]]
# Output: [0,1]
# Explanation: In this case favoriteCompanies[2]=["facebook","google"] is a subset of favoriteCompanies[0]=["leetcode","google","facebook"], therefore, the answer is [0,1].
#
# Example 3:
#
# Input: favoriteCompanies = [["leetcode"],["google"],["facebook"],["amazon"]]
# Output: [0,1,2,3]
#
# Constraints:
#
#     1 <= favoriteCompanies.length <= 100
#     1 <= favoriteCompanies[i].length <= 500
#     1 <= favoriteCompanies[i][j].length <= 20
#     All strings in favoriteCompanies[i] are distinct.
#     All lists of favorite companies are distinct, that is, If we sort alphabetically each list then favoriteCompanies[i] != favoriteCompanies[j].
#     All strings consist of lowercase English letters only.
#
# ---
# 
# The brute force method is to create sets, and to compare sets using issubset.
# the constaints are quite manageable, with a max of 50k companies
# so bf might pass
# 
# LEETCODE: Accepted (88 ms, 33 MB)

# mu 0.17

class Solution
  def peopleIndexes(favoriteCompanies: [[str]]) -> [int]
    fc = [set(x) for x in favoriteCompanies]
    ret res = []
    for >i in fc
      is_subset = false
      for >j in fc
        if i != j
          if fc[i].issubset(fc[j])
            is_subset = true
            break
      if not is_subset
        res <- i


sol = Solution()

print(sol.peopleIndexes([['leetcode', 'google', 'facebook'], ['google', 'microsoft'], ['google', 'facebook'], ['google'], ['amazon']]))  # [0,1,4]

assert sol.peopleIndexes([['leetcode', 'google', 'facebook'], ['google', 'microsoft'], ['google', 'facebook'], ['google'], ['amazon']]) == [0, 1, 4]
assert sol.peopleIndexes([['leetcode', 'google', 'facebook'], ['leetcode', 'amazon'], ['facebook', 'google']]) == [0, 1]
assert sol.peopleIndexes([['leetcode'], ['google'], ['facebook'], ['amazon']]) == [0, 1, 2, 3]
assert sol.peopleIndexes([['a']]) == [0]
assert sol.peopleIndexes([['a'], ['a']]) == []
assert sol.peopleIndexes([['a'], ['b'], ['a', 'b']]) == [2]
assert sol.peopleIndexes([['a', 'b', 'c'], ['a', 'b'], ['b', 'c'], ['c']]) == [0]
assert sol.peopleIndexes([['a', 'b'], ['a', 'b'], ['a', 'b']]) == []
assert sol.peopleIndexes([['a' * 20], ['b' * 20], ['a' * 20, 'b' * 20]]) == [2]
assert sol.peopleIndexes([['a' + str(i) for i in 0..<500], ['a' + str(i) for i in 0..<499]]) == [0]
assert sol.peopleIndexes([['a' + str(i) for i in 0..<500], ['a' + str(i) for i in 0..<500]]) == []
assert sol.peopleIndexes([['a' + str(i) for i in 0..<500], ['a' + str(i) for i in 250..<750]]) == [0, 1]
assert sol.peopleIndexes([['a'], ['a', 'b'], ['a', 'b', 'c'], ['a', 'b', 'c', 'd']]) == [3]
assert sol.peopleIndexes([['a', 'b', 'c', 'd'], ['b', 'c', 'd'], ['c', 'd'], ['d']]) == [0]
assert sol.peopleIndexes([['a', 'b', 'c'], ['b', 'c'], ['a', 'b'], ['a']]) == [0]
