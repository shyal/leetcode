"""
URL: https://leetcode.com/problems/minimum-height-trees/description/?envType=problem-list-v2&envId=vn57k9wr

310. Minimum Height Trees

A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [a_i, b_i] indicates that there is an undirected edge between the two nodes a_i and b_i in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h)) are called minimum height trees (MHTs).

Return a list of all MHTs' root labels. You can return the answer in any order.

The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

Example 1:

Input: n = 4, edges = [[1,0],[1,2],[1,3]]
Output: [1]
Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.

Example 2:

Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
Output: [3,4]

Constraints:

    1 <= n <= 2 * 10^4
    edges.length == n - 1
    0 <= a_i, b_i < n
    a_i != b_i
    All the pairs (a_i, b_i) are distinct.
    The given input is guaranteed to be a tree and there will be no repeated edges.
"""


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))
        
        graph = defaultdict(list)
        degrees = [0] * n
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
            degrees[a] += 1
            degrees[b] += 1
        
        queue = deque([i for i in range(n) if degrees[i] == 1])
        
        remaining = n
        
        while remaining > 2:
            level_size = len(queue)
            remaining -= level_size
            
            for _ in range(level_size):
                leaf = queue.popleft()
                
                for neighbor in graph[leaf]:
                    degrees[neighbor] -= 1
                    if degrees[neighbor] == 1:
                        queue.append(neighbor)
        
        return list(queue)

sol = Solution()

#print(sol.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]]))  # [1]

assert sorted(sol.findMinHeightTrees(4, [[1,0],[1,2],[1,3]])) == [1]
assert sorted(sol.findMinHeightTrees(6, [[3,0],[3,1],[3,2],[3,4],[5,4]])) == [3,4]
# assert sorted(sol.findMinHeightTrees(1, [])) == [0]
# assert sorted(sol.findMinHeightTrees(2, [[0,1]])) == [0,1]
# assert sorted(sol.findMinHeightTrees(3, [[0,1],[1,2]])) == [1]
# assert sorted(sol.findMinHeightTrees(4, [[0,1],[1,2],[2,3]])) == [1,2]
# assert sorted(sol.findMinHeightTrees(5, [[0,1],[0,2],[0,3],[0,4]])) == [0]
# assert sorted(sol.findMinHeightTrees(4, [[0,1],[1,2],[0,3]])) == [0,1]
# assert sorted(sol.findMinHeightTrees(7, [[0,1],[1,2],[1,3],[2,4],[3,5],[4,6]])) == [1,2]
# assert sorted(sol.findMinHeightTrees(5, [[0,1],[0,2],[2,3],[0,4]])) == [0]
