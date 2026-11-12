# URL: https://leetcode.com/problems/most-frequent-subtree-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 508. Most Frequent Subtree Sum
#
# Given the root of a binary tree, return the most frequent subtree sum. If there is a tie, return all the values with the highest frequency in any order.
#
# The subtree sum of a node is defined as the sum of all the node values formed by the subtree rooted at that node (including the node itself).
#
# Example 1:
#
# Input: root = [5,2,-3]
# Output: [2,-3,4]
#
# Example 2:
#
# Input: root = [5,2,-5]
# Output: [2]
#
# Constraints:
#
#     The number of nodes in the tree is in the range [1, 10^4].
#     -10^5 <= Node.val <= 10^5
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# perform a dfs, and store the subtree sum (including the value of the node) into a counter.
# this is done by returning the subtree sum of each subtree, adding them together with the value
# of the node, and storing them into a counter.
# 
# then, look for the value with the highest frequency. if there is one, then return that.
# if there isn't one, then return all the values in what seems to be postorder.
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# self.counter = counter()
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# HINT: The last part is wrong: when there is a tie you should not return all sums in postorder. After counting, find the highest frequency value first, then keep only the sums whose count equals that value, like the sums 2, -3 and 4 in Example 1 which all appear once.
# STAGE 3 of 3 - the code. Replace each pseudocode line with code. Then run make solved.
# LEETCODE: Accepted (6 ms, 22.2 MB)


# mu 0.17

class Solution
  def findFrequentTreeSum(root: TreeNode?) -> [int]
    self.counter = counter()
    {
      (n) ->
        if not n
          return 0
        lss = mu n.left
        rss = mu n.right
        sss = n.val + lss + rss
        self.counter[sss] += 1
        return sss
    }(root)
    if len self.counter > 1
      hfv = self.counter.most_common()[0][1]
      return [k for k, v in self.counter.items() if v == hfv]
    else
      return [self.counter.most_common()[0][0]]

sol = Solution()

root = build_tree([5, 2, -3])
print(root)

print(sol.findFrequentTreeSum(root))  # [2,-3,4]

assert sorted(sol.findFrequentTreeSum(build_tree([5, 2, -3]))) == sorted([2, -3, 4])
assert sol.findFrequentTreeSum(build_tree([5, 2, -5])) == [2]
assert sol.findFrequentTreeSum(build_tree([1])) == [1]
