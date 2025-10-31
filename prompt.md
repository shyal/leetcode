i'm thinking of changing my strategy, and want to discuss with you about this. currently my goal is to solve 7 a day, and of course review questions on my learning queue. i use anki but sporadically. i'm thinking of changing to emphasizing quality over quantity. So you could generate say 5 or 10 cards a day which i'd remember 100% faultlessly, and we could plan reviews, or varations. like you could prepare a list of problems for me to tackle on any given day, not necessarily covering new questions, but more reinforcing what i know, and general problem solving. thoughts? 


Here is my LeetCode solve history (most recent last):

# 2025-09-15 15:16: 1518. Water Bottles (Easy):

```python3
class Solution:

    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        drink = numBottles
        remainder = 0
        while numBottles + remainder >= numExchange:
            (numBottles, remainder) = divmod(numBottles + remainder, numExchange)
            drink += numBottles
        return drink
```

---------------------

# 2025-09-15 16:06: 504. Base 7 (Easy):

```python3
class Solution:

    def convertToBase7(self, num: int) -> str:
        if num == 0:
            return '0'
        res = ''
        sign = 1 if num >= 0 else -1
        num *= sign
        while num > 0:
            (val, r) = divmod(num, 7)
            res += str(r)
            num = val
        res = ('-' if sign == -1 else '') + res[::-1]
        return res
```

---------------------

# 2025-09-15 16:19: 867. Transpose Matrix (Easy):

```python3
"""
1 2 3
4 5 6
7 8 9


"""

class Solution:

    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        return [list(x) for x in zip(*matrix)]
```

---------------------

# 2025-09-15 16:33: 1470. Shuffle the Array (Easy):

```python3
from itertools import chain

class Solution:

    def shuffle(self, nums: List[int], n: int) -> List[int]:
        return [*chain(*[[nums[i], nums[n + i]] for i in range(n)])]
```

---------------------

# 2025-09-16 08:16: 872. Leaf-Similar Trees (Easy):

```python3
class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:

    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:

        def dfs(node, leaves):
            if not node:
                return
            is_leaf = node.left == node.right == None
            if is_leaf:
                leaves.append(node.val)
                return
            dfs(node.left, leaves)
            dfs(node.right, leaves)
        leaves1 = []
        leaves2 = []
        dfs(root1, leaves1)
        dfs(root2, leaves2)
        return leaves1 == leaves2
```

---------------------

# 2025-09-16 11:03: 498. Diagonal Traverse (Medium):

```python3
class Dir:
    up = 0
    down = 1

class Solution:

    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:

        def diag_up(row, col):
            ret = []
            r = row
            c = col
            while r >= 0 and c <= len(mat[0]) - 1:
                ret.append(mat[r][c])
                c += 1
                r -= 1
            return ret

        def diag_down(row, col):
            return [*reversed(diag_up(row, col))]

        def diag(row, col, d):
            return diag_up(row, col) if d == Dir.up else diag_down(row, col)
        ret = []
        d = Dir.up
        rows = [*range(len(mat))] + [len(mat) - 1] * (len(mat[0]) - 1)
        cols = [0] * len(mat) + [*range(1, len(mat[0]))]
        inds = [*zip(rows, cols)]
        for (r, c) in inds:
            ret.extend(diag(r, c, d))
            d = Dir.up if d == Dir.down else Dir.down
        return ret
```

---------------------

# 2025-09-17 06:29: 167. Two Sum II - Input Array Is Sorted (Medium):

```python3
class Solution:

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1
```

---------------------

# 2025-09-17 08:25: 1071. Greatest Common Divisor of Strings (Easy):

```python3
from itertools import zip_longest

class Solution:

    def gcdOfStrings(self, str1: str, str2: str) -> str:

        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for (a, b) in zip_longest(r, r[1:])]
        batch_match = lambda x: all([a == b for (a, b) in zip(x, x[1:])])
        for n in range(len(str2), 0, -1):
            (b1, b2) = (batched(str1, n), batched(str2, n))
            if b1[0] == b2[0] and batch_match(b1) and batch_match(b2):
                return b1[0]
        return ''
```

---------------------

# 2025-09-17 09:57: 1431. Kids With the Greatest Number of Candies (Easy):

```python3
class Solution:

    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        _max = max(candies)
        return [x + extraCandies >= _max for x in candies]
```

---------------------

# 2025-09-17 10:34: 605. Can Place Flowers (Easy):

```python3
class Solution:

    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        added = 0
        for i in range(len(flowerbed)):
            left_slot_free = i == 0 or flowerbed[i - 1] == 0
            right_slot_free = i == len(flowerbed) - 1 or flowerbed[i + 1] == 0
            if (left_slot_free and right_slot_free) and flowerbed[i] == 0:
                if added < n:
                    flowerbed[i] = 1
                    added += 1
        return added == n
```

---------------------

# 2025-09-17 10:50: 345. Reverse Vowels of a String (Easy):

```python3
class Solution:

    def reverseVowels(self, s: str) -> str:
        s = list(s)
        v = set('aeiouAEIOU')
        left = 0
        right = len(s) - 1
        while left <= right:
            left_is_vowel = s[left] in v
            right_is_vowel = s[right] in v
            if left_is_vowel and right_is_vowel:
                (s[left], s[right]) = (s[right], s[left])
                left += 1
                right -= 1
                continue
            if not left_is_vowel:
                left += 1
            if not right_is_vowel:
                right -= 1
        return ''.join(s)
```

---------------------

# 2025-09-17 10:57: 151. Reverse Words in a String (Medium):

```python3
class Solution:

    def reverseWords(self, s: str) -> str:
        return ' '.join((x for x in reversed(s.split())))
```

---------------------

# 2025-09-17 11:44: 238. Product of Array Except Self (Medium):

```python3
from operator import mul

class Solution:

    def productExceptSelfLetters(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x)]
        left = ['1'] + acc(nums[:-1])
        right = (['1'] + acc(nums[1:][::-1]))[::-1]
        return [a + b for (a, b) in zip(left, right)]

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x, mul)]
        left = [1] + acc(nums[:-1])
        right = ([1] + acc(nums[1:][::-1]))[::-1]
        return [a * b for (a, b) in zip(left, right)]
```

## notes: 

OK so with this problem, it really helps to use variables instead of numbers, and think in terms
of output.

So with [a, b, c, d], the output is:

bcd, acd, abd, abc

so accumulating from the left, we get:

1, a, ab, abc

accumulating from the right, we get:

dcb dc d  1

multiplying these two gives us:

bcd, acd, abd, abc

---------------------

# 2025-09-17 13:37: 443. String Compression (Medium):

```python3
from itertools import groupby
from itertools import chain

class Solution:

    def compress(self, chars: List[str]) -> int:
        a = [*chain(*[(char, *str(count)) if count > 1 else char for (char, count) in [(c, len([*it])) for (c, it) in groupby(chars)]])]
        chars[:len(a)] = a
        return len(a)
```

---------------------

# 2025-09-17 13:53: 283. Move Zeroes (Easy):

```python3
class Solution:

    def moveZeroes(self, nums: List[int]) -> None:
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                (nums[write], nums[read]) = (nums[read], nums[write])
                write += 1
```

---------------------

# 2025-09-17 14:05: 392. Is Subsequence (Easy):

```python3
class Solution:

    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        i = 0
        for c in t:
            if s[i] == c:
                i += 1
            if i == len(s):
                return True
        return False
```

---------------------

# 2025-09-17 14:49: 1679. Max Number of K-Sum Pairs (Medium):

```python3
from collections import defaultdict

class Solution:

    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        (left, right) = (0, len(nums) - 1)
        count = 0
        while left < right:
            total = nums[left] + nums[right]
            if total == k:
                left += 1
                right -= 1
                count += 1
            elif total > k:
                right -= 1
            else:
                left += 1
        return count
```

---------------------

# 2025-09-18 05:46: 643. Maximum Average Subarray I (Easy):

```python3
class Solution:

    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        right = k - 1
        av = sum(nums[:k]) / k
        _max = av
        for i in range(k, len(nums)):
            av -= nums[i - k] / k
            av += nums[i] / k
            _max = max(_max, av)
        return int(_max * 10 ** 5) / 10 ** 5
```

---------------------

# 2025-09-18 06:30: 1456. Maximum Number of Vowels in a Substring of Given Length (Medium):

```python3
class Solution:

    def maxVowels(self, s: str, k: int) -> int:
        v = set('aeiou')
        _max = sum([x in v for x in s[:k]])
        count = _max
        for i in range(k, len(s)):
            count -= s[i - k] in v
            count += s[i] in v
            _max = max(_max, count)
        return _max
```

---------------------

# 2025-09-18 08:17: 1004. Max Consecutive Ones III (Medium):

```python3
class Solution:

    def longestOnes(self, nums: List[int], k: int) -> int:
        one_count = 0
        zeros = 0
        ones = 0
        left = 0
        _max = 0
        for right in range(len(nums)):
            v = nums[right]
            ones += v == 1
            zeros += v == 0
            if zeros > k:
                ones -= nums[left] == 1
                zeros -= nums[left] == 0
                left += 1
            _max = max(_max, ones + zeros)
        return _max
```

---------------------

# 2025-09-18 10:46: 1732. Find the Highest Altitude (Easy):

```python3
class Solution:

    def largestAltitude(self, gain: List[int]) -> int:
        altitude = 0
        _max = 0
        for g in gain:
            altitude += g
            _max = max(altitude, _max)
        return _max
```

---------------------

# 2025-09-18 12:27: 724. Find Pivot Index (Easy):

```python3
class Solution:

    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        prefix_sum = 0
        for (i, n) in enumerate(nums):
            total -= n
            if prefix_sum == total:
                return i
            prefix_sum += n
        return -1
```

---------------------

# 2025-09-18 12:32: 2215. Find the Difference of Two Arrays (Easy):

```python3
class Solution:

    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        return [list(nums1 - nums2), list(nums2 - nums1)]
```

---------------------

# 2025-09-18 12:39: 1207. Unique Number of Occurrences (Easy):

```python3
from collections import Counter

class Solution:

    def uniqueOccurrences(self, arr: List[int]) -> bool:
        occurrences = [count for (val, count) in Counter(arr).items()]
        return len(occurrences) == len(set(occurrences))
```

---------------------

# 2025-09-18 13:49: 1657. Determine if Two Strings Are Close (Medium):

```python3
from collections import Counter

class Solution:

    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False
        (c1, c2) = (dict(Counter(word1)), dict(Counter(word2)))
        letters_match = [*sorted(c1.keys())] == [*sorted(c2.keys())]
        counts_match = [*sorted(c1.values())] == [*sorted(c2.values())]
        return letters_match and counts_match
```

---------------------

# 2025-09-18 14:45: 2215. Find the Difference of Two Arrays (Easy):

```python3
class Solution:

    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        return [list(nums1 - nums2), list(nums2 - nums1)]
```

---------------------

# 2025-09-18 14:58: 2390. Removing Stars From a String (Medium):

```python3
class Solution:

    def removeStars(self, s: str) -> str:
        stack = []
        for c in s:
            if c != '*':
                stack.append(c)
            elif stack:
                stack.pop()
        return ''.join(stack)
```

---------------------

# 2025-09-18 15:53: 735. Asteroid Collision (Medium):

```python3
class Solution:

    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        while True:
            stack = []
            smash = False
            for ast in asteroids:
                if not stack:
                    stack.append(ast)
                    continue
                else:
                    prev = stack[-1]
                    prev_dir = prev >= 0
                    ast_dir = ast >= 0
                    on_collision_course = prev_dir == 1 and ast_dir == 0
                    prev_smash = on_collision_course and abs(prev) <= abs(ast)
                    ast_smash = on_collision_course and abs(prev) >= abs(ast)
                    if prev_smash and stack:
                        stack.pop()
                        smash = True
                    if not ast_smash:
                        stack.append(ast)
            if not smash:
                break
            asteroids = stack[:]
        return stack
```

---------------------

# 2025-09-19 05:49: 933. Number of Recent Calls (Easy):

```python3
from collections import deque

class Solution:

    def main(self):

        class RecentCounter:

            def __init__(self):
                self.pings = deque()

            def ping(self, t: int) -> int:
                self.pings.append(t)
                while True:
                    if self.pings[0] < self.pings[-1] - 3000:
                        self.pings.popleft()
                    else:
                        break
                return len(self.pings)
        return RecentCounter
```

---------------------

# 2025-09-19 07:04: 2095. Delete the Middle Node of a Linked List (Medium):

```python3
from linked_list_utils import build_linked_list, print_linked_list, get_list_values
from typing import Optional

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:

    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head
        prev = head
        count = 0
        while fast.next:
            if count % 2 == 0:
                prev = slow
                slow = slow.next
            count += 1
            fast = fast.next
        prev.next = slow.next
        count += 1
        return head if count > 1 else None
```

---------------------

# 2025-09-19 09:46: 206. Reverse Linked List (Easy):

```python3
from typing import Optional
import linked_list_utils as llutils

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        it = head.next
        trailing = head
        while it:
            it_next = it.next
            it.next = trailing
            trailing = it
            it = it_next
        head.next = None
        return trailing
```

---------------------

# 2025-09-19 11:02: 2130. Maximum Twin Sum of a Linked List (Medium):

```python3
from typing import Optional
import linked_list_utils as llutils

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:

    def pairSum(self, head: Optional[ListNode]) -> int:
        (it, prev, count) = (head, None, 0)
        while it:
            count += 1
            it.prev = prev
            prev = it
            it = it.next
        (right, left, _max) = (prev, head, 0)
        while True:
            _max = max(_max, left.val + right.val)
            if left.next == right:
                break
            (left, right) = (left.next, right.prev)
        return _max
```

---------------------

# 2025-09-19 11:16: 104. Maximum Depth of Binary Tree (Easy):

```python3
from typing import List, Optional
from tree_utils import build_tree

class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:

    def maxDepth(self, root: Optional[TreeNode]) -> int:

        def helper(node):
            return 1 + max(helper(node.left) if node.left else 0, helper(node.right) if node.right else 0)
        return helper(root) if root else 0
```

---------------------

# 2025-09-20 08:32: 1448. Count Good Nodes in Binary Tree (Medium):

```python3
class Solution:

    def goodNodes(self, root: Optional[TreeNode]) -> int:

        def helper(node, max_val):
            if not node:
                return 0
            count = 0
            if node.val >= max_val:
                node.color = 'blue'
                count = 1
            _max = max(node.val, max_val)
            return count + helper(node.left, _max) + helper(node.right, _max)
        return helper(root, root.val) if root else 0
```

---------------------

# 2025-09-20 11:19: 1372. Longest ZigZag Path in a Binary Tree (Medium):

```python3
class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:

    def longestZigZag(self, root: Optional[TreeNode]) -> int:

        def helper(node, r=0, l=0):
            if node:
                _max[0] = max(_max[0], max(r, l))
                if node.left:
                    helper(node.left, r=0, l=r + 1)
                if node.right:
                    helper(node.right, r=l + 1, l=0)
        _max = [0]
        helper(root)
        return _max[0]
```

---------------------

# 2025-09-20 13:07: 338. Counting Bits (Easy):

```python3
from typing import List

class Solution:

    def countBits(self, n: int) -> List[int]:

        def count_ones(n):
            count = 0
            while n:
                count += n & 1
                n >>= 1
            return count
        return [count_ones(i) for i in range(n + 1)]
```

---------------------

# 2025-09-20 13:22: 136. Single Number (Easy):

```python3
from typing import List
from functools import reduce
from operator import xor

class Solution:

    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)
```

---------------------

# 2025-09-20 15:37: 1318. Minimum Flips to Make a OR b Equal to c (Medium):

```python3
class Solution:

    def minFlips(self, a: int, b: int, c: int) -> int:
        count = 0
        while a or b or c:
            (_a, _b, _c) = (a & 1, b & 1, c & 1)
            _ab = _a + _b
            count += not _ab if _c else _ab
            (a, b, c) = (a >> 1, b >> 1, c >> 1)
        return count
```

---------------------

# 2025-09-20 19:11: 208. Implement Trie (Prefix Tree) (Medium):

```python3
class Node:

    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else {}

class Solution:

    def main(self):

        class Trie:

            def __init__(self):
                self.data = set([])
                self.g = Node('head')

            def insert(self, word: str) -> None:
                it = self.g
                for c in word:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        nn = Node(c)
                        it.children[c] = nn
                        it = nn
                it.children['.'] = Node('.')

            def search(self, word: str) -> bool:
                it = self.g
                for c in word:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        return False
                return '.' in it.children

            def startsWith(self, prefix: str) -> bool:
                it = self.g
                for c in prefix:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        return False
                return True
        return Trie
```

---------------------

# 2025-09-21 07:42: 1268. Search Suggestions System (Medium):

```python3
from typing import List

class Solution:

    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        res = []
        for i in range(len(searchWord)):
            prefix = searchWord[:i + 1]
            res.append([*sorted(filter(lambda x: x.startswith(prefix), products))][:3])
        return res
```

---------------------

# 2025-09-21 14:30: 739. Daily Temperatures (Medium):

```python3
from typing import List

class Solution:

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        answer = [0] * len(temperatures)
        for (i, temp) in enumerate(temperatures):
            if not stack:
                stack.append((temp, i))
            elif stack[-1][0] < temp:
                while stack and stack[-1][0] < temp:
                    (j_temp, j) = stack.pop()
                    answer[j] = i - j
                stack.append((temp, i))
            else:
                stack.append((temp, i))
        return answer
```

---------------------

# 2025-09-22 08:43: 334. Increasing Triplet Subsequence (Medium):

```python3
from typing import List

class Solution:

    def increasingTriplet(self, nums: List[int]) -> bool:
        a = float('inf')
        b = float('inf')
        for n in nums:
            if n <= a:
                a = n
            elif n <= b:
                b = n
            else:
                return True
        return False
```

---------------------

# 2025-09-22 15:17: 841. Keys and Rooms (Medium):

```python3
from typing import List

class Solution:

    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        def open(i):
            if i in seen:
                return 0
            seen.add(i)
            keys = rooms[i]
            visited = 1
            for room in keys:
                visited += open(room)
            return visited
        seen = set([])
        return open(0) == len(rooms)
```

---------------------

# 2025-09-22 15:53: 547. Number of Provinces (Medium):

```python3
from typing import List

class Solution:

    def findCircleNum(self, isConnected: List[List[int]]) -> int:

        def dfs(city):
            if city in seen:
                return 0
            seen.add(city)
            visited = 1
            for c in range(len(isConnected[city])):
                if isConnected[city][c]:
                    visited += dfs(c)
            return visited
        seen = set([])
        count = 0
        for i in range(len(isConnected)):
            visited = dfs(i)
            count += visited > 0
        return count
```

---------------------

# 2025-09-22 17:16: 1466. Reorder Routes to Make All Paths Lead to the City Zero (Medium):

```python3
from typing import List
from collections import defaultdict

class Solution:

    def minReorder(self, n: int, connections: List[List[int]]) -> int:

        def dfs(city):
            seen.add(city)
            neighbouring_cities = G[city].keys()
            flips = 0
            for neighbouring_city in neighbouring_cities:
                if neighbouring_city in seen:
                    continue
                if G[city][neighbouring_city] == 1:
                    flips += 1
                flips += dfs(neighbouring_city)
            return flips
        seen = set([])
        G = defaultdict(dict)
        for (c1, c2) in connections:
            G[c1][c2] = 1
            G[c2][c1] = 0
        return dfs(0)
```

---------------------

# 2025-09-23 09:14: 1926. Nearest Exit from Entrance in Maze (Medium):

```python3
class Solution:

    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:

        def ij_in_maze(i, j, maze):
            return 0 <= i < len(maze) and 0 <= j < len(maze[0])
        D = deque()
        D.append((entrance, 0))
        maze[entrance[0]][entrance[1]] = '+'
        while D:
            (curr, dist) = D.popleft()
            is_v_edge = curr[0] == 0 or curr[0] == len(maze) - 1
            is_h_edge = curr[1] == 0 or curr[1] == len(maze[0]) - 1
            if (is_h_edge or is_v_edge) and curr != entrance:
                return dist
            prod = [[curr[0] - 1, curr[1]], [curr[0] + 1, curr[1]], [curr[0], curr[1] - 1], [curr[0], curr[1] + 1]]
            prod = [*filter(lambda x: ij_in_maze(x[0], x[1], maze) and maze[x[0]][x[1]] == '.' and (x != entrance), prod)]
            for new_pos in prod:
                maze[new_pos[0]][new_pos[1]] = '+'
                D.append([new_pos, dist + 1])
        return -1
```

---------------------

# 2025-09-23 11:40: 994. Rotting Oranges (Medium):

```python3
"""
Notes:

One solution is to linearly search for all rotten oranges, load them onto a deque
and perform a BFS. Let's handle the case where we begin with multiple rotten oranges
because 



"""
from collections import deque
from typing import List
from itertools import chain

class Solution:

    def orangesRotting(self, grid: List[List[int]]) -> int:
        D = deque()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    D.append((i, j, 0))
        time = 0
        while D:
            (ri, rj, s) = D.popleft()
            time = max(time, s)
            val = grid[ri][rj]
            if ri - 1 >= 0 and grid[ri - 1][rj] == 1:
                grid[ri - 1][rj] = 2
                D.append([ri - 1, rj, s + 1])
            if ri + 1 < len(grid) and grid[ri + 1][rj] == 1:
                grid[ri + 1][rj] = 2
                D.append([ri + 1, rj, s + 1])
            if rj - 1 >= 0 and grid[ri][rj - 1] == 1:
                grid[ri][rj - 1] = 2
                D.append([ri, rj - 1, s + 1])
            if rj + 1 < len(grid[0]) and grid[ri][rj + 1] == 1:
                grid[ri][rj + 1] = 2
                D.append([ri, rj + 1, s + 1])
        has_ones = any((x == 1 for x in chain(*grid)))
        return -1 if has_ones else time
```

---------------------

# 2025-09-23 14:25: 215. Kth Largest Element in an Array (Medium):

```python3
class Solution:

    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for n in nums:
            heappush(heap, n)
            if len(heap) > k:
                heappop(heap)
        return heap[0]
```

---------------------

# 2025-09-24 07:37: 374. Guess Number Higher or Lower (Easy):

```python3
def guess(num):
    global pick
    if num > pick:
        return -1
    elif num < pick:
        return 1
    else:
        return 0

class Solution:

    def guessNumber(self, n: int) -> int:
        (left, right) = (0, n)
        while left <= right:
            mid = (left + right) // 2
            res = guess(mid)
            if res == -1:
                right = mid - 1
            elif res == 1:
                left = mid + 1
            else:
                return mid
pick = 6
n = 10
```

---------------------

# 2025-09-24 10:28: 2300. Successful Pairs of Spells and Potions (Medium):

```python3
from typing import List
from functools import cache

class Solution:

    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:

        def bin_search_first_valid_spell(spell, success):
            (left, right) = (0, len(potions) - 1)
            ans = 0
            while left <= right:
                mid = (left + right) // 2
                res = potions[mid] * spell
                if res < success:
                    left = mid + 1
                elif res >= success:
                    right = mid - 1
                    if potions[mid - 1] * spell < success:
                        break
            return mid if potions[mid] * spell >= success else None

        @cache
        def get_num_valid_spells(spell, success):
            first_idx = bin_search_first_valid_spell(spell, success)
            if first_idx is None:
                return 0
            else:
                return len(potions) - first_idx
        potions.sort()
        count = []
        for spell in spells:
            num = get_num_valid_spells(spell, success)
            count.append(num)
        return count
```

---------------------

# 2025-09-24 12:59: 435. Non-overlapping Intervals (Medium):

```python3
from typing import List

class Solution:

    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        prev = intervals[0]
        count = 1
        for interval in intervals:
            overlap = interval[0] < prev[1]
            if not overlap:
                prev = interval
                count += 1
        return len(intervals) - count
```

---------------------

# 2025-09-24 13:41: 452. Minimum Number of Arrows to Burst Balloons (Medium):

```python3
from typing import List

class Solution:

    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda x: x[1])
        prev = points[0]
        count = 1
        for i in range(1, len(points)):
            has_overlap = points[i][0] <= prev[1]
            if not has_overlap:
                count += 1
                prev = points[i]
        return count
```

---------------------

# 2025-09-24 14:30: 17. Letter Combinations of a Phone Number (Medium):

```python3
from typing import List

class Solution:

    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        letters = ['', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
        digits = [int(x) for x in digits]
        letters = [letters[i] for i in digits]

        def dfs(depth=0, path=''):
            if depth == len(digits):
                combos.append(path)
                return
            for (i, l) in enumerate(letters[depth]):
                dfs(depth + 1, path + l)
        combos = []
        dfs()
        return combos
```

---------------------

# 2025-09-25 12:18: 216. Combination Sum III (Medium):

```python3
class Solution:

    def brute_force(self, k, n):
        from itertools import combinations
        combs = combinations(range(1, 10), k)
        return [list(x) for x in combs if sum(x) == n and len(x) == len(set(x))]

    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        nums = [i for i in range(1, 10)]

        def dfs(i, curr, prefix=0):
            if len(curr) == k and prefix == n:
                res.append(curr[:])
                return
            for j in range(i, len(nums)):
                curr.append(nums[j])
                prefix += nums[j]
                dfs(j + 1, curr, prefix)
                prefix -= curr.pop()
        res = []
        dfs(0, [])
        return res
```

---------------------

# 2025-09-25 12:47: 1137. N-th Tribonacci Number (Easy):

```python3
from functools import cache

class Solution:

    @cache
    def tribonacci(self, n: int) -> int:
        if n <= 1:
            return n
        elif n == 2:
            return 1
        return self.tribonacci(n - 3) + self.tribonacci(n - 2) + self.tribonacci(n - 1)
```

---------------------

# 2025-09-25 14:00: 746. Min Cost Climbing Stairs (Easy):

```python3
from typing import List

class Solution:

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        for i in range(len(cost) - 3, -1, -1):
            cost[i] = cost[i] + min(cost[i + 1], cost[i + 2])
        return min(cost[0], cost[1])
```

---------------------

# 2025-09-25 14:58: 199. Binary Tree Right Side View (Medium):

```python3
from typing import Optional, List

class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:

        def dfs(node, depth=0):
            if not node:
                return
            if depth > data['max_depth']:
                right_side.append(node.val)
                data['max_depth'] = depth
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)
        data = {'max_depth': -1}
        right_side = []
        dfs(root, 0)
        return right_side
```

---------------------

# 2025-09-25 15:51: 1161. Maximum Level Sum of a Binary Tree (Medium):

```python3
from typing import Optional, List
from collections import defaultdict

class Solution:

    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        D = defaultdict(int)

        def dfs(node, depth):
            if node:
                D[depth] += node.val
                dfs(node.left, depth + 1)
                dfs(node.right, depth + 1)
        dfs(root, 1)
        levels = [*D.items()]
        max_val = max(levels, key=lambda x: x[1])[1]
        max_levels = [*filter(lambda x: x[1] == max_val, levels)]
        sorted_max_levels = sorted(max_levels, key=lambda x: x[0])
        return next(iter(sorted_max_levels))[0]
```

---------------------

# 2025-09-25 16:12: 700. Search in a Binary Search Tree (Easy):

```python3
class Solution:

    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return
        if root.val == val:
            return root
        if val < root.val and root.left:
            return self.searchBST(root.left, val)
        elif val > root.val and root.right:
            return self.searchBST(root.right, val)
```

---------------------

# 2025-09-26 07:24: 215. Kth Largest Element in an Array (Medium):

```python3
class Solution:

    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for n in nums:
            heappush(heap, n)
            if len(heap) > k:
                heappop(heap)
        return heap[0]
```

---------------------

# 2025-09-26 09:52: 198. House Robber (Medium):

```python3
"""

Let's think of more examples

Example 2:

Input: nums = [1, 1, 5, 5, 5, 6]

"""
from typing import List

class Solution:

    def rob(self, nums: List[int]) -> int:
        _max = 0
        for i in range(len(nums) - 1, -1, -1):
            v = nums[i]
            nums[i] = max(v + nums[i + 2] if i + 2 < len(nums) else v, v + nums[i + 3] if i + 3 < len(nums) else v)
            _max = max(nums[i], _max)
        return _max
```

---------------------

# 2025-09-26 14:08: 875. Koko Eating Bananas (Medium):

```python3
"""
Input: piles = [3,6,7,11], h = 8
Output: 4

[3,6,7,11] -> [3,6,7,7] hour 1, eats 4 from pils 4
[3,6,7,7]  -> [3,6,7,3] hour 2, eats 4 from pils 4
[3,2,7,3]  -> [3,2,3,3] hour 3, eats 4 from pils 3
[3,6,7,3]  -> [3,2,7,3] hour 4, eats 4 from pils 2
[3,2,3,3]  -> [3,2,3,3] takes another 4 hours (1 hour per pile)


[3,6,7,11] -> [3,6,7,3] (2) (divmod 11 = 2, 3)
[3,6,7,11] -> [3,6,3,3] (1)
[3,2,3,11] -> [3,6,3,3] (1)


"""
from functools import reduce
from typing import List

class Solution:

    def hoursToEatPiles(self, piles, k):
        return reduce(lambda a, v: a + v // k + (1 if v % k else 0), piles, 0)

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left = 1
        right = sum(piles)
        while left <= right:
            k = (left + right) // 2
            hours = self.hoursToEatPiles(piles, k)
            if hours <= h:
                right = k - 1
            elif hours > h:
                left = k + 1
        return left
```

---------------------

# 2025-09-26 16:30: 450. Delete Node in a BST (Medium):

```python3
import random

class Solution:

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        def find_rightmost_leaf(root):
            if root and root.right:
                return find_rightmost_leaf(root.right)
            return root

        def helper(parent, node, key):
            if node:
                if node.val == key:
                    if (rightmost := (find_rightmost_leaf(node.left) or node.left)):
                        rightmost.right = node.right
                    if node == parent.left:
                        parent.left = node.left or node.right
                    else:
                        parent.right = node.left or node.right
                elif key < node.val:
                    helper(node, node.left, key)
                elif key > node.val:
                    helper(node, node.right, key)
        dummy = TreeNode(-10000000000.0, right=root)
        helper(dummy, root, key)
        return dummy.right
```

---------------------

# 2025-09-27 11:12: 72. Edit Distance (Medium):

```python3
from functools import cache

class Solution:

    def minDistance(self, word1: str, word2: str) -> int:

        @cache
        def dp_str(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return dp_str(a[:-1], b[:-1])
            add = dp_str(a, b[:-1])
            rem = dp_str(a[:-1], b)
            sub = dp_str(a[:-1], b[:-1])
            return min(add, rem, sub) + 1

        @cache
        def dp(i, j):
            if i < 0:
                return j + 1
            if j < 0:
                return i + 1
            if word1[i] == word2[j]:
                return dp(i - 1, j - 1)
            add = dp(i, j - 1)
            rem = dp(i - 1, j)
            sub = dp(i - 1, j - 1)
            return min(add, rem, sub) + 1
        return dp(len(word1) - 1, len(word2) - 1)
```

---------------------

# 2025-09-27 11:31: 11. Container With Most Water (Medium):

```python3
class Solution:

    def maxArea(self, height: List[int]) -> int:
        (L, R) = (0, len(height) - 1)
        _max = 0
        while L < R:
            h = min(height[L], height[R])
            area = h * (R - L)
            _max = max(_max, area)
            if height[L] < height[R]:
                L += 1
            else:
                R -= 1
        return _max
```

---------------------

# 2025-09-27 15:48: 112. Path Sum (Easy):

```python3
class Solution:

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        def dfs(prefix, node):
            if not node:
                return False
            is_leaf = node.left is None and node.right is None
            return prefix + node.val == targetSum if is_leaf else dfs(prefix + node.val, node.left) or dfs(prefix + node.val, node.right)
        return dfs(0, root)
```

---------------------

# 2025-09-27 16:18: 58. Length of Last Word (Easy):

```python3
class Solution:

    def lengthOfLastWord(self, s: str) -> int:
        if not s:
            return 0
        first_non_space = None
        first_space_after_non_space = None
        _len = 0
        for i in range(len(s) - 1, -1, -1):
            if first_non_space is None and s[i] != ' ':
                first_non_space = i
                _len += 1
            elif first_non_space is not None and s[i] != ' ':
                _len += 1
            elif first_non_space is not None and s[i] == ' ':
                break
        return _len
```

---------------------

# 2025-09-27 16:48: 796. Rotate String (Easy):

```python3
from itertools import islice, chain

class Solution:

    def rotateString(self, s: str, goal: str) -> bool:
        if s == goal:
            return True
        if len(s) != len(goal):
            return False

        def rotate(s, r):
            return chain(islice(s, r, None), islice(s, None, r))
        for shift in range(len(s)):
            r = rotate(s, shift)
            if all((a == b for (a, b) in zip(r, goal))):
                return True
        return False
```

---------------------

# 2025-09-27 16:54: 217. Contains Duplicate (Easy):

```python3
class Solution:

    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))
```

---------------------

# 2025-09-28 07:21: 111. Minimum Depth of Binary Tree (Easy):

```python3
class Solution:

    def minDepth(self, root: Optional[TreeNode]) -> int:

        def dfs(node, depth):
            if not node:
                return float('inf')
            is_leaf = node.left is None and node.right is None
            if is_leaf:
                return depth
            return min(dfs(node.left, depth + 1), dfs(node.right, depth + 1))
        return dfs(root, 1) if root else 0
```

---------------------

# 2025-09-28 09:04: 819. Most Common Word (Easy):

```python3
from collections import Counter
rem = set("!?',;.")

class Solution:

    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        banned = set(banned)
        tmp = []
        for c in paragraph:
            if c in rem:
                tmp.append(' ')
            else:
                tmp.append(c.lower())
        count = dict(Counter(''.join(tmp).split()))
        res = next(iter(max(count.items(), key=lambda x: x[1] if x[0] not in banned else 0)), '')
        return res if res not in banned else ''
```

---------------------

# 2025-09-28 09:22: 830. Positions of Large Groups (Easy):

```python3
from itertools import groupby
from collections import namedtuple

class Solution:

    def largeGroupPositions(self, s: str) -> List[List[int]]:
        G = groupby(s)
        Interval = namedtuple('Interval', ['chars', 'interval'])
        intervals = []
        i = 0
        for (letter, it) in G:
            val = ''.join(it)
            if len(val) >= 3:
                interval = Interval(val, [i, i + len(val) - 1])
                intervals.append(interval)
            i += len(val)
        intervals.sort(key=lambda x: x.interval[0])
        return [interval.interval for interval in intervals]
```

---------------------

# 2025-09-28 09:59: 1493. Longest Subarray of 1's After Deleting One Element (Medium):

```python3
class Solution:

    def longestSubarray(self, nums: List[int]) -> int:
        pass
```

---------------------

# 2025-09-29 08:15: 26. Remove Duplicates from Sorted Array (Easy):

```python3
class Solution:

    def bf0(self, nums):
        s = set(nums)
        nums[:len(s)] = [*sorted(list(s))]
        return len(s)

    def removeDuplicates(self, nums: List[int]) -> int:
        write = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[write] = nums[i]
                write += 1
        return write
```

## notes: 

--------

 w  r
[0, 1, 1, 1, 2, 2, 3, 3, 4]
    x.    x. x     x.    x

---------------------

# 2025-09-29 09:09: 101. Symmetric Tree (Easy):

```python3
class Solution:

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:

        def dfs(node, depth=0, _dir=0):
            if not node:
                yield None
                return
            yield node.val
            choice = (node.left, node.right)
            yield from dfs(choice[_dir], depth + 1, _dir)
            if depth > 0:
                yield from dfs(choice[not _dir], depth + 1, _dir)
        return all((a == b for (a, b) in zip(dfs(root, _dir=0), dfs(root, _dir=1))))
```

## notes: 

[1]
   ┌───┴───┐
  [2]     [2]
 ┌─┴─┐   ┌─┴─┐
[3] [4] [4] [3]

  [1]
 ┌─┴─┐
[2] [2]
 ┐   ┐
[3] [3]

---------------------

# 2025-09-29 10:14: 108. Convert Sorted Array to Binary Search Tree (Easy):

```python3
class Solution:

    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:

        def helper(start, end):
            if start < end:
                mid = (start + end) // 2
                return TreeNode(nums[mid], helper(start, mid), helper(mid + 1, end))
        return helper(0, len(nums))
```

## notes: 

---

  [2]
 ┌─┴─┐
[1] [4]
 /   /
[0] [3]


[1]
 /
[0]


     [3]
   ┌──┴──┐
  [1]   [5]
 ┌─┴─┐   /
[0] [2] [4]


                                 [20]
               ┌──────────────────┴───────────────────┐
              [10]                                   [30]
       ┌───────┴────────┐                   ┌─────────┴─────────┐
      [5]              [15]                [25]                [35]
   ┌───┴───┐       ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
  [2]     [8]     [13]      [18]      [23]      [28]      [33]      [38]
 ┌─┴─┐   ┌─┴─┐   ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐
[1] [4] [7] [9] [12] [14] [17] [19] [22] [24] [27] [29] [32] [34] [37] [39]
 /   /   /       /         /         /         /         /         /
[0] [3] [6]     [11]      [16]      [21]      [26]      [31]      [36]

---------------------

# 2025-09-29 12:00: 110. Balanced Binary Tree (Easy):

```python3
class Solution:

    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        def dfs(node, height):
            if not node:
                yield (height, True)
                return (height, True)
            else:
                (left_height, left_balanced) = (yield from dfs(node.left, height + 1))
                (right_height, right_balanced) = (yield from dfs(node.right, height + 1))
                (height, is_balanced) = (max(left_height, right_height), abs(left_height - right_height) <= 1 and left_balanced and right_balanced)
                yield (height, is_balanced)
                return (height, is_balanced)
        return all((x[1] for x in dfs(root, 0)))
```

---------------------

# 2025-09-29 12:27: 118. Pascal's Triangle (Easy):

```python3
from itertools import pairwise

class Solution:

    def generate(self, numRows: int) -> List[List[int]]:
        res = [[1], [1, 1]]
        prev = res[-1]
        for _ in range(numRows - 2):
            res.append([1] + [a + b for (a, b) in pairwise(prev)] + [1])
            prev = res[-1]
        return res[:numRows]
```

---------------------

# 2025-09-29 12:52: 144. Binary Tree Preorder Traversal (Easy):

```python3
class Solution:

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        def dfs(node):
            if not node:
                return
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)
        res = []
        dfs(root)
        return res
```

---------------------

# 2025-09-29 15:22: 566. Reshape the Matrix (Easy):

```python3
from itertools import chain
from itertools import zip_longest

def batched(s, n=1):
    r = list(range(0, len(s), n))
    return [s[a:b] for (a, b) in zip_longest(r, r[1:])]

class Solution:

    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        if r == len(mat) and c == len(mat[0]) or r * c != len(mat) * len(mat[0]):
            return mat
        return batched([*chain(*mat)], c)
```

---------------------

# 2025-09-29 15:57: 168. Excel Sheet Column Title (Easy):

```python3
from string import ascii_uppercase

class Solution:

    def convertToTitle(self, columnNumber: int) -> str:
        res = ''
        while columnNumber:
            columnNumber -= 1
            mod = columnNumber % 26
            res = ascii_uppercase[mod] + res
            columnNumber //= 26
        return res
```

---------------------

# 2025-09-29 16:18: 202. Happy Number (Easy):

```python3
from functools import reduce

class Solution:

    def isHappy(self, n: int) -> bool:
        nums = set([])
        while n != 1:
            digits = [int(x) for x in str(n)]
            n = reduce(lambda acc, v: acc + v * v, digits, 0)
            nums_size = len(nums)
            nums.add(n)
            if nums_size == len(nums):
                break
        return n == 1
```

---------------------

# 2025-09-29 16:46: 219. Contains Duplicate II (Easy):

```python3
class Solution:

    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        nums = [*enumerate(nums)]
        nums.sort(key=lambda x: x[1])
        for i in range(1, len(nums)):
            if nums[i][1] == nums[i - 1][1] and abs(nums[i][0] - nums[i - 1][0]) <= k:
                return True
        return False
```

---------------------

# 2025-09-30 04:00: 263. Ugly Number (Easy) (time: 7m 05):

```python3
class Solution:

    def isUgly(self, n: int) -> bool:
        if n == 0:
            return False
        if n == 1:
            return True
        v = n
        while v != 1:
            for d in [2, 3, 5]:
                if v % d == 0:
                    v = v // d
                    break
            else:
                return False
        return True
```

---------------------

# 2025-09-30 04:07: 258. Add Digits (Easy) (time: 4m 15):

```python3
class Solution:

    def addDigits(self, num: int) -> int:
        while num >= 10:
            num = sum((int(x) for x in str(num)))
        return num
```

---------------------

# 2025-09-30 04:10: 242. Valid Anagram (Easy) (time: 1m 51):

```python3
from collections import Counter

class Solution:

    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

---------------------

# 2025-09-30 06:17: 226. Invert Binary Tree (Easy) (time: 6m 24):

```python3
class Solution:

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            (node.right, node.left) = (node.left, node.right)
        dfs(root)
        return root
```

---------------------

# 2025-09-30 06:53: 225. Implement Stack using Queues (Easy) (time: 8m 22):

```python3
class Solution:

    def func():
        pass
from collections import deque

class MyStack:

    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)

    def pop(self) -> int:
        return self.q.pop()

    def top(self) -> int:
        return self.q[-1]

    def empty(self) -> bool:
        return len(self.q) == 0
```

---------------------

# 2025-09-30 07:29: 222. Count Complete Tree Nodes (Easy) (time: 25m 49):

```python3
class Solution:

    def countNodes(self, root: Optional[TreeNode]) -> int:

        def dfs(node, height=0, direction=None):
            if not node:
                if direction is None:
                    return 0
                return height - 1
            if direction is None:
                left_height = dfs(node.left, height + 1, 0)
                right_height = dfs(node.right, height + 1, 1)
                if left_height == right_height:
                    return 2 ** (left_height + 1) - 1
                else:
                    left_count = dfs(node.left, 0, None)
                    right_count = dfs(node.right, 0, None)
                    node.val = left_count + right_count + 1
                    return left_count + right_count + 1
            elif direction == 0:
                return dfs(node.left, height + 1, direction)
            elif direction == 1:
                return dfs(node.right, height + 1, direction)
        res = dfs(root) if root else 0
        return res
```

---------------------

# 2025-09-30 07:56: 203. Remove Linked List Elements (Easy) (time: 6m 54):

```python3
class Solution:

    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy_head = ListNode(None, head)
        it = dummy_head
        while it.next:
            if it.next.val == val:
                it.next = it.next.next
            else:
                it = it.next
        return dummy_head.next
```

---------------------

# 2025-09-30 08:42: 21. Merge Two Sorted Lists (Easy) (time: 25m 13):

```python3
class Solution:

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        l1 = list1
        l2 = list2

        def pop(L):
            if L:
                next = L.next
                L.next = None
                return (L, next)
            return (None, None)

        def pop_smallest(l1, l2):
            if l1 and l2:
                if l1.val < l2.val:
                    (popped, new_l1) = pop(l1)
                    return (popped, new_l1, l2)
                else:
                    (popped, new_l2) = pop(l2)
                    return (popped, l1, new_l2)
            else:
                l = l1 or l2
                (popped, new) = pop(l)
                return (popped, new, None)
        it = ListNode(-1)
        dummy_head = it
        while it:
            (popped, l1, l2) = pop_smallest(l1, l2)
            it.next = popped
            it = it.next
        return dummy_head.next
```

---------------------

# 2025-09-30 09:06: 141. Linked List Cycle (Easy) (time: 9m 37):

```python3
class Solution:

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        (slow, fast) = (head, head)
        while head and slow.next and fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
```

---------------------

# 2025-09-30 09:24: 234. Palindrome Linked List (Easy) (time: 12m 23):

```python3
class Solution:

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        it = head
        prev = None
        while it:
            it.prev = prev
            prev = it
            it = it.next
        it = head
        end = prev
        while it != end:
            if end.val != it.val:
                return False
            if it.next == end or end.prev == it:
                return it.next.val == end.prev.val
            it = it.next
            end = end.prev
        return True
```

---------------------

# 2025-09-30 09:56: 876. Middle of the Linked List (Easy) (time: 9m 40):

```python3
class Solution:

    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        (slow, fast) = (head, head)
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
```

---------------------

# 2025-09-30 10:15: 70. Climbing Stairs (Easy) (time: 2m 32):

```python3
from functools import cache

class Solution:

    def climbStairs(self, n: int) -> int:

        @cache
        def dp(n):
            if n <= 3:
                return n
            return dp(n - 1) + dp(n - 2)
        return dp(n)
```

---------------------

# 2025-09-30 10:51: 64. Minimum Path Sum (Medium) (time: 29m 50):

```python3
class Solution:

    def minPathSum(self, grid: List[List[int]]) -> int:
        dp = [0] * len(grid[0])
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if j > 0:
                    from_left_cost = dp[j - 1]
                    from_current_cost = grid[i][j]
                    from_top_cost = dp[j]
                    dp[j] = from_current_cost + min(from_left_cost, from_top_cost if i > 0 else float('inf'))
                else:
                    dp[j] += grid[i][j]
        return dp[-1]
```

---------------------

# 2025-09-30 13:05: 63. Unique Paths II (Medium) (time: 49m 17):

```python3
class Solution:

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        g = obstacleGrid
        dp = [1] * len(g[0])
        if 1 in g[0]:
            block = g[0].index(1)
            for i in range(len(dp)):
                if i >= block:
                    dp[i] = 0
        for i in range(1, len(g)):
            if g[i][0] == 1:
                dp[0] = 0
            for j in range(1, len(g[0])):
                dp[j] = dp[j] + dp[j - 1] if g[i][j] == 0 else 0
        return dp[-1]
```

---------------------

# 2025-09-30 13:15: 121. Best Time to Buy and Sell Stock (Easy) (time: 4m 2):

```python3
class Solution:

    def maxProfit(self, prices: List[int]) -> int:
        _max = 0
        _min = float('inf')
        for (i, p) in enumerate(prices):
            _min = min(_min, p)
            _max = max(_max, p - _min)
        return _max
```

---------------------

# 2025-09-30 13:51: 53. Maximum Subarray (Medium) (time: 20m 0):

```python3
class Solution:

    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = 0
        _max = float('-inf')
        for (i, n) in enumerate(nums):
            current_sum = max(n, n + current_sum) if i > 0 else n
            _max = max(_max, current_sum)
        return _max
```

---------------------

# 2025-10-01 08:19: 1025. Divisor Game (Easy) (time: 60m 45):

```python3
class Solution:

    def divisorGame(self, n: int) -> bool:
        return n % 2 == 0
```

## notes: 

------

Had to look up the solution for this. It may or may not fall in the DP arena, as
one can also take a pure maths approach.

---------------------

# 2025-10-01 08:35: 509. Fibonacci Number (Easy) (time: 2m 35):

```python3
from functools import cache

class Solution:

    @cache
    def fib(self, n: int) -> int:
        if n <= 1:
            return n
        return self.fib(n - 1) + self.fib(n - 2)
```

---------------------

# 2025-10-01 09:15: 9. Palindrome Number (Easy) (time: 32m 32):

```python3
class Solution:

    def isPalindrome(self, x: int) -> bool:
        neg = x < 0
        if neg:
            return False
        st = str(x)
        for i in range(len(st) // 2):
            if st[i] != st[len(st) - i - 1]:
                return False
        return True
```

---------------------

# 2025-10-01 09:31: 20. Valid Parentheses (Easy) (time: 9m 26):

```python3
class Solution:

    def isValid(self, s: str) -> bool:
        d = {')': '(', ']': '[', '}': '{'}
        stack = []
        for c in s:
            if c not in d:
                stack.append(c)
            else:
                if not stack:
                    return False
                if stack.pop() != d[c]:
                    return False
        return len(stack) == 0
```

---------------------

# 2025-10-01 09:46: 1. Two Sum (Easy) (time: 5m 41):

```python3
class Solution:

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for (i, n) in enumerate(nums):
            complement = target - n
            if complement in d:
                return [d[complement], i]
            d[n] = i
```

---------------------

# 2025-10-01 10:16: 88. Merge Sorted Array (Easy) (time: 26m 55):

```python3
class Solution:

    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        (A, B) = (nums1, nums2)
        a = len(A) - len(B) - 1
        b = len(B) - 1
        end = len(A) - 1

        def consume(a, b):
            if a >= 0 and b >= 0:
                (na, nb) = (A[a], B[b])
                if na > nb:
                    return (a - 1, b, na)
                else:
                    return (a, b - 1, nb)
            elif a >= 0:
                return (a - 1, b, A[a])
            else:
                return (a, b - 1, B[b])
        while end >= 0:
            (a, b, nums1[end]) = consume(a, b)
            end -= 1
```

## notes: 

-------

             a
A = [1,2,3,4,5,0,0,0,0,0]
B = [3,4,5,6,7]
             b


             a
A = [1,2,3,4,5,0,0,0,0,7]
B = [3,4,5,6,7]
           b

             a
A = [1,2,3,4,5,0,0,0,6,7]
B = [3,4,5,6,7]
         b

           a
A = [1,2,3,4,5,0,0,5,6,7]
B = [3,4,5,6,7]
         b

etc.

---------------------

# 2025-10-01 10:46: 66. Plus One (Easy) (time: 20m 21):

```python3
class Solution:

    def plusOne(self, digits: List[int]) -> List[int]:
        carry = False
        for i in range(len(digits) - 1, -1, -1):
            d = digits[i]
            is_end = i == len(digits) - 1
            if is_end:
                if d < 9:
                    digits[i] += 1
                else:
                    carry = True
                    digits[i] = 0
            elif carry:
                if d == 9:
                    digits[i] = 0
                    carry = True
                else:
                    digits[i] += 1
                    carry = False
            elif not carry:
                break
        if digits[0] == 0:
            digits.insert(0, 1)
        return digits
```

## notes: 

-----

1 2 3

This case is easy, we just add to the digits[-1] the problem arises if it's 9

1 2 9

In this case, we need to set digits[-1] to 0

1 2 0

then focus on the second to last element, and increment it

1 3 0

so the real edgecase is when it's all 9s

9 9 9

- carry = False
- iterate from right to left
    - if it's the last index:
        - if d < 9
            - add 1
        - else
            - carry = True
            - d = 0
    - elif carry:
        - if d == 9
            - d = 0
    - elif not carry:
        break

- if nums[0] == 0
    - insert 0 at front of digits

---------------------

# 2025-10-01 11:06: 119. Pascal's Triangle II (Easy) (time: 13m 47):

```python3
class Solution:

    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex == 0:
            return [1]
        dp = [1, 1]
        for i in range(2, rowIndex + 1):
            dp = [1] + [a + b for (a, b) in pairwise(dp)] + [1]
        return dp
```

## notes: 

----

so the rows are:

1
1
12
132
146

---------------------

# 2025-10-01 11:32: 13. Roman to Integer (Easy) (time: 20m 45):

```python3
vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
rules = {'I': 'VX', 'X': 'LC', 'C': 'DM'}

class Solution:

    def romanToInt(self, s: str) -> int:

        def func(acc, i):
            c = s[i]
            if c in rules and i != len(s) - 1 and (s[i + 1] in rules[c]):
                return acc - vals[c]
            return acc + vals[c]
        return reduce(func, range(len(s) - 1, -1, -1), 0)
```

## notes: 

-----

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

    I can be placed before V (5) and X (10) to make 4 and 9.
    X can be placed before L (50) and C (100) to make 40 and 90.
    C can be placed before D (500) and M (1000) to make 400 and 900.

---------------------

# 2025-10-01 11:41: 14. Longest Common Prefix (Easy) (time: 6m 25):

```python3
class Solution:

    def longestCommonPrefix(self, strs: List[str]) -> str:
        return ''.join((x[0] for x in takewhile(lambda x: all([a == b for (a, b) in pairwise(x)]), zip(*strs))))
```

---------------------

# 2025-10-01 12:56: 28. Find the Index of the First Occurrence in a String (Easy) (time: 12m 46):

```python3
class Solution:

    def strStr(self, haystack: str, needle: str) -> int:
        for i in range(len(haystack) - len(needle) + 1):
            all_match = True
            for j in range(len(needle)):
                if haystack[i + j] != needle[j]:
                    all_match = False
                    break
            if all_match:
                return i
        return -1
```

---------------------

# 2025-10-02 06:13: 94. Binary Tree Inorder Traversal (Easy) (time: 2m 20):

```python3
class Solution:

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        res = []
        dfs(root)
        return res
```

---------------------

# 2025-10-02 06:32: 145. Binary Tree Postorder Traversal (Easy) (time: 1m 11):

```python3
class Solution:

    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            ret.append(node.val)
        ret = []
        dfs(root)
        return ret
```

---------------------

# 2025-10-02 06:39: 100. Same Tree (Easy) (time: 7m 58):

```python3
class Solution:

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

        def dfs(n1, n2):
            if n1 and (not n2) or (n2 and (not n1)):
                return False
            if not (n1 and n2):
                return True
            return n1.val == n2.val and dfs(n1.left, n2.left) and dfs(n1.right, n2.right)
        return dfs(p, q)
```

## notes: 

Ok need to think about this one a little bit. In the dfs function:

- If one root exists, but not the other, they differ, so return false
- if they're both none, return true because that's valid
- if they both exist
    - recursively call dfs on both children, since they'll return
    the base cases, `and` the result from both

---------------------

# 2025-10-02 07:33: 98. Validate Binary Search Tree (Medium) - learning:

```python3
class Solution:

    def isValidBST(self, root: TreeNode) -> bool:

        def dfs(node, lower, upper):
            if not node:
                return True
            if lower < node.val < upper:
                left_valid = dfs(node.left, lower, node.val)
                right_valid = dfs(node.right, node.val, upper)
                return left_valid and right_valid
            else:
                return False
        return dfs(node=root, lower=float('-inf'), upper=float('inf'))
```

## notes: 

Create a dfs function, which takes the value of the parent, and whether we're a left
or right child.

Perform the check (gt, or lt), and recursively call this dfs function on both left and right
children.

The bases case is if we're None, in which case return True since an empty tree is a valid BST.

---------------------

# 2025-10-02 08:48: 105. Construct Binary Tree from Preorder and Inorder Traversal (Medium) - learning:

```python3
class Solution:

    def buildTreeSimple(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        def dfs(pos=0):
            val = preorder[pos]
            val_inorder_index = inorder.index(val)
            left_vals = inorder[:val_inorder_index]
            right_vals = inorder[val_inorder_index + 1:]
            node = TreeNode(val, TreeNode(left_vals[0]), TreeNode(right_vals[0]))
            return node
        return dfs()

    def buildTree(self, preorder, inorder):
        if inorder:
            ind = inorder.index(preorder.pop(0))
            root = TreeNode(inorder[ind])
            root.left = self.buildTree(preorder, inorder[0:ind])
            root.right = self.buildTree(preorder, inorder[ind + 1:])
            return root

def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    res = []
    q = [root]
    while q:
        node = q.pop(0)
        res.append(node.val if node else None)
        if node:
            q.append(node.left)
            q.append(node.right)
    while res and res[-1] is None:
        res.pop()
    return res
```

## notes: 

Starting with a simple example:

tree = sol.buildTree([3, 9, 20], [9, 3, 20])

We notice that 3 is at the start of the list in the pre order, so the root node
and in the in-order, it's in the middle of the list, so 9 must be the left child
and 20 the right

tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

Here we notice the same thing, 3 only has 1 left child, and 3 right children.
Then if we move on to 20, we notice that it to has 1 left and 1 right child.

This perhapse suggests recursion, with certain bounds within the list to check
children / subtrees.

I might build a solution for the simple version of the tree, then expand it for
the more complex versions.

For the simple version:

- start with first node of inorder (3)
- get its index in in-order
    - use remaining values for left and right child

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def dfs(pos=0):
            val = preorder[pos]
            val_inorder_index = inorder.index(val)
            left_vals = inorder[:val_inorder_index]
            right_vals = inorder[val_inorder_index + 1 :]
            node = TreeNode(val, TreeNode(left_vals[0]), TreeNode(right_vals[0]))
            return node

        return dfs()

  [3]
 ┌─┴─┐
[9] [20]

OK that rebuilds the tree nicely. Now let's think about how we'll deal with the more complex
example.

tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

Clearly we need to call dfs recursively, and pass bounds for the indices, or sublists
to make it even simpler.

Failed. Looked up solution.

---------------------

# 2025-10-02 09:27: 106. Construct Binary Tree from Inorder and Postorder Traversal (Medium) (time: 32m 47):

```python3
class Solution:

    def buildTree(self, inorder, postorder):
        if not inorder:
            return
        index = inorder.index(postorder.pop())
        node = TreeNode(inorder[index])
        left = self.buildTree(inorder[:index], postorder[:index])
        right = self.buildTree(inorder[index + 1:], postorder[index:])
        node.left = left
        node.right = right
        return node
```

## notes: 

What might work is popping the post order traversal (3) then getting its index
in the inorder traversal.

In order:

What's on the left of the index is the left subtree.
what's on the right of the index is the right subtree.

Post order:

The left subtree is the size of the inorder left subtree
The right subtree is what's left of the list

Tip for future solves: what really helped was using colour coding for left and right subtrees
on my paper notes. 3 colours, one for the root, one for the left, and one for the right.
This made spotting the pattern of which sublists matched which subtrees
a lot easier.

---------------------

# 2025-10-02 10:26: 109. Convert Sorted List to Binary Search Tree (Medium) (time: 16m 58):

```python3
class Solution:

    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        vals = []
        it = head
        while it:
            vals.append(it.val)
            it = it.next

        def dfs(left, right):
            if left > right:
                return
            mid = (left + right) // 2
            val = vals[mid]
            node = TreeNode(val)
            node.left = dfs(left, mid - 1)
            node.right = dfs(mid + 1, right)
            return node
        return dfs(0, len(vals) - 1)
```

## notes: 

Interesting challenge. Quite tricky as i'm not even sure i can built a balanced BST with a sorted list. Might be worth working on that first before working with the linked list.

Ok i guess to build a BST with a sorted list, one starts from the middle, adds that as a node, then uses the left and right subarrays recursively. So i could simply convert the LL to an array, but that's extra space.

If i pass the middle of the LL, then i'll have to iterate over and over to find the mid point for the sublists, so that's less time efficient. I think i'll go with O(N) space, and keep time efficient.

Hmm tricky to decide between time and space on this one. Both seem interesting, though constant space sounds like the more 'fun' approach, while O(N) space is less interesting.

Ah NVM let's keep it simple first. So O(N) space.

Ok so i guess this can be done in O(N)

Ok solved. This definitely felt easy.

---------------------

# 2025-10-02 11:01: 114. Flatten Binary Tree to Linked List (Medium) (time: 28m 43):

```python3
class Solution:

    def flatten(self, root: Optional[TreeNode]) -> None:

        def pre_order(node):
            if not node:
                return
            res.append(node.val)
            pre_order(node.left)
            pre_order(node.right)
        if not root:
            return
        res = []
        pre_order(root)
        new = TreeNode(-1, None, None)
        it = new
        for r in res:
            it.right = TreeNode(r)
            it = it.right
        root.right = new.right.right if new.right else None
        root.left = None
```

## notes: 

Hmm i didn't understand the question initially, i didn't realize the tree
has to be mutated, rather than return a new linked list.

Hmm not super happy with this solve. It feels a little 'brute force'.

Tip: read the question properly next time.

---------------------

# 2025-10-02 11:51: 257. Binary Tree Paths (Easy) (time: 10m 37):

```python3
class Solution:

    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:

        def dfs(node, path=[]):
            if not node:
                return
            copy = path + [str(node.val)]
            dfs(node.left, copy)
            dfs(node.right, copy)
            if node.left is None and node.right is None:
                paths.append('->'.join(copy))
        paths = []
        dfs(root)
        return paths
```

---------------------

# 2025-10-02 12:13: 129. Sum Root to Leaf Numbers (Medium) (time: 8m 27):

```python3
class Solution:

    def sumNumbers(self, root: Optional[TreeNode]) -> int:

        def dfs(node, val=0):
            if not node:
                return 0
            left = dfs(node.left, val * 10 + node.val)
            right = dfs(node.right, val * 10 + node.val)
            if node.left is None and node.right is None:
                return val * 10 + node.val
            return left + right
        res = dfs(root)
        return res
```

---------------------

# 2025-10-02 12:30: 404. Sum of Left Leaves (Easy) (time: 7m 36):

```python3
class Solution:

    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:

        def dfs(node, dir=None):
            if not node:
                return 0
            if node.left is None and node.right is None and (dir is False):
                return node.val
            return dfs(node.left, False) + dfs(node.right, True)
        res = dfs(root)
        return res
```

---------------------

# 2025-10-02 12:52: 437. Path Sum III (Medium) - learning:

```python3
class Solution:

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        pass
```

## notes: 

I'm going to mark this as "learning" because even though i solved it recently (with some help) i'm drawing a blank.

I know there's a way of checking if a contiguous subarray contains a sum, but it's slipped my mind.

Also i know the idea is basically to use this subarray sum technique with the tree, but i would need to review those
basic subarray sum mechanics before jumping into this question.

---------------------

# 2025-10-02 13:34: 560. Subarray Sum Equals K (Medium) - learning:

```python3
class Solution:

    def subarraySum(self, nums: List[int], k: int) -> int:
        res = 0
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        for n in nums:
            prefix += n
            if prefix - k in D:
                res += D[prefix - k]
            D[prefix] += 1
        return res
```

## notes: 

I completely blanked on prefix sum, which is unacceptable. I really feel i need to go to town
on prefix sum type problems, slowly ramping up complexity, else i'll keep forgetting it.

---------------------

# 2025-10-02 13:51: 303. Range Sum Query - Immutable (Easy) (time: 11m 22):

```python3
class NumArray:

    def __init__(self, nums: List[int]):
        self.prefix = [*accumulate(nums), 0]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right] - self.prefix[left - 1]
```

## notes: 

Ok this one felt obvious, simply accumulate values, using itertools
then subtract the [0 -> left -1] from [0 to right].
even figured out a neat trick to avoid bounds checking.

---------------------

# 2025-10-03 05:18: 304. Range Sum Query 2D - Immutable (Medium) (time: 9m 51):

```python3
class Solution:

    def dummy(self):
        pass

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.sums = [[*accumulate(row)] + [0] for row in matrix]

    def sumRange(self, i, j, row):
        return self.sums[row][j] - self.sums[row][i - 1]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum((self.sumRange(col1, col2, row) for row in range(row1, row2 + 1)))
matrix = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
matrix = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
```

---------------------

# 2025-10-03 05:22: 1480. Running Sum of 1d Array (Easy) (time: 1m 3):

```python3
class Solution:

    def runningSum(self, nums: List[int]) -> List[int]:
        return [*accumulate(nums)]
```

---------------------

# 2025-10-03 05:37: 1991. Find the Middle Index in Array (Easy) (time: 11m 20):

```python3
class Solution:

    def findMiddleIndex(self, nums: List[int]) -> int:
        (left_sum, right_sum) = (0, sum(nums))
        for i in range(len(nums)):
            right_sum -= nums[i]
            if left_sum == right_sum:
                return i
            left_sum += nums[i]
        return -1
```

## notes: 

[2, 3, -1, 8, 4]

I guess the approach is to start with the left sum, and right sum. Then iterate to
increment / decrement them, and compare them.

---------------------

# 2025-10-03 06:08: 977. Squares of a Sorted Array (Easy) (time: 28m 42):

```python3
class Solution:

    def bruteForce(self, nums: List[int]) -> List[int]:
        squared = [x ** 2 for x in nums]
        return [*sorted(squared)]

    def take(self, A, B, a, b):
        if a < len(A) and b < len(B):
            if A[a] < B[b]:
                return (A[a], a + 1, b)
            else:
                return (B[b], a, b + 1)
        elif a == len(A) and b < len(B):
            return (B[b], a, b + 1)
        elif b == len(B) and a < len(A):
            return (A[a], a + 1, b)
        return (None, None, None)

    def sortedSquares(self, nums: List[int]) -> List[int]:
        i = bisect_left(nums, 0)
        left = [-x for x in nums[:i][::-1]]
        right = nums[i:]
        arr = []
        (a, b) = (0, 0)
        while True:
            (val, a, b) = self.take(left, right, a, b)
            if val is None:
                break
            arr.append(val)
        return [x ** 2 for x in arr]
```

## notes: 

I'm trying to think of the followup:

[-4, -1, 0, 3, 10]
[16, 1, 0, 9, 100]

What i'm noticing is that since we're squaring, we can ignore the sign. But i still can't quite figure
how to sort those elements in O(n).

Oh ok we can look for where the elements go from negative to positive, then merge them.

         v
[-4, -1, 0, 3, 10]

right: 0, 3, 10
left: -1, -4

merged: 0, -1, 3, -4, 10

I'm not really happy with how i merged the arrays. Would be great to revisit some array
problems that force me to merge things in place.

---------------------

# 2025-10-03 06:45: 27. Remove Element (Easy) (time: 14m 49):

```python3
class Solution:

    def removeElement(self, nums: List[int], val: int) -> int:
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                (nums[read], nums[write]) = (nums[write], nums[read])
                write += 1
        return write
```

## notes: 

r
[0,1,2,2,3,0,4,2]
   w

   r
[1,0,2,2,3,0,4,2]
     w

---------------------

# 2025-10-03 07:06: 80. Remove Duplicates from Sorted Array II (Medium) (time: 17m 20):

```python3
class Solution:

    def removeDuplicates(self, nums: List[int]) -> int:
        nums[:] = [*chain(*[[num] * min(2, len([*it])) for (num, it) in groupby(nums)])]
        return len(nums)
```

## notes: 

doing this in place seems complex, so i might just use a more
brute force approach, then optimize

---------------------

# 2025-10-03 08:38: 15. 3Sum (Medium) - learning:

```python3
class Solution:

    def twoSum(self, nums, target=0, exclude=-1):
        (D, indices) = (dd(set), [])
        for (i, n) in enumerate(nums):
            if i == exclude:
                continue
            comp = target - n
            if comp in D:
                matches = [(j, i) if i > j else (j, i) for j in D[comp] if j != exclude]
                if matches:
                    indices.extend(matches)
            D[n].add(i)
        return indices

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set([])
        for (i, n) in enumerate(nums):
            for ts in self.twoSum(nums, -n, i):
                res.add(tuple(sorted([nums[i], nums[ts[0]], nums[ts[1]]])))
        return list((list(x) for x in res))[::-1]
```

## notes: 

Ok since we need the indices, i'm thinking of using the hash map approach, so
first build the two sums variant, then use two sum for three sum.

We need to track all occurrances of two sum, so use a defaultdict of set.

So my solution works, but has a TLE with long input.

I botched this one... because i didn't notice the requirements was for unique
values rather than unique indices.

I'd rather revisit it later.

---------------------

# 2025-10-03 11:25: 974. Subarray Sums Divisible by K (Medium) - learning (time: 25723m 50):

```python3
class Solution:

    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        D = defaultdict(int)
        D[0] = 1
        prefix_mod = 0
        res = 0
        for n in nums:
            prefix_mod = (prefix_mod + n) % k
            res += D[prefix_mod]
            D[prefix_mod] += 1
        return res
```

## notes: 

This feels like magic to me. I barely remembered the subarray sum == k solution,
which i get when i step through it but still feels a touch like magic (starting to get it
but keep forgetting).

This solution however i had to look up, and feels entirely magical.

---------------------

# 2025-10-03 11:45: 290. Word Pattern (Easy) (time: 12m 25):

```python3
class Solution:

    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        d = {}
        for (a, b) in zip(pattern, words):
            if a in d:
                if d[a] != b:
                    return False
            d[a] = b
        return len(pattern) == len(words) and len(d.keys()) == len(set(d.values()))
```

---------------------

# 2025-10-03 11:58: 3541. Find Most Frequent Vowel and Consonant (Easy) (time: 9m 39):

```python3
from collections import Counter

class Solution:

    def maxFreqSum(self, s: str) -> int:
        vowels = set('aeiou')
        freq = defaultdict(int)
        for c in s:
            freq[c] += 1
        freq = list(freq.items())
        freq.sort(key=lambda x: -x[1])
        return next((x[1] for x in freq if x[0] in vowels), 0) + next((x[1] for x in freq if x[0] not in vowels), 0)
```

---------------------

# 2025-10-03 12:04: 1512. Number of Good Pairs (Easy) (time: 4m 24):

```python3
class Solution:

    def numIdenticalPairs(self, nums: List[int]) -> int:
        return sum((i < j and nums[i] == nums[j] for (i, j) in combinations(range(len(nums)), 2)))
```

---------------------

# 2025-10-03 15:24: 543. Diameter of Binary Tree (Easy) - learning (time: 20m 0):

```python3
class Solution:

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diam = 0

        def dfs(node):
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            self.diam = max(self.diam, left + right)
            return max(left, right) + 1
        dfs(root)
        return self.diam
```

## notes: 

I think the diameter is essentially the max of the depth on the left subtree
and and the right subtree. This definition works recursively.

---------------------

# 2025-10-04 02:47: 3467. Transform Array by Parity (Easy) (time: 15m 29):

```python3
class Solution:

    def transformArray(self, nums: List[int]) -> List[int]:
        for i in range(len(nums)):
            nums[i] = int(bool(nums[i] % 2))
        nums.sort()
        return nums
```

---------------------

# 2025-10-04 02:54: 2011. Final Value of Variable After Performing Operations (Easy) (time: 5m 7):

```python3
ops = {'--X': lambda x: x - 1, 'X--': lambda x: x - 1, 'X++': lambda x: x + 1, '++X': lambda x: x + 1}

class Solution:

    def finalValueAfterOperations(self, operations: List[str]) -> int:
        return reduce(lambda acc, val: ops[val](acc), operations, 0)
```

---------------------

# 2025-10-04 02:57: 3668. Restore Finishing Order (Easy) (time: 1m 49):

```python3
class Solution:

    def recoverOrder(self, order: List[int], friends: List[int]) -> List[int]:
        friends = set(friends)
        return [x for x in order if x in friends]
```

---------------------

# 2025-10-04 03:05: 3190. Find Minimum Operations to Make All Elements Divisible by Three (Easy) (time: 5m 20):

```python3
class Solution:

    def minimumOperations(self, nums: List[int]) -> int:
        return sum((int(bool(x % 3)) for x in nums))
```

## notes: 

Ok first let's figure how to compute the number of ops to make a number divisible by 3.

0 % 3 == 0
1 % 3 == 1
2 % 3 == 2
3 % 3 == 0
4 % 3 == 1
5 % 3 == 2
6 % 3 == 0
7 % 3 == 1
8 % 3 == 2
9 % 3 == 0

Looks like we're always just 1 operation away from being divisible by 3, IF we're not
already divisible by 3.

---------------------

# 2025-10-04 03:09: 1672. Richest Customer Wealth (Easy) (time: 1m 43):

```python3
class Solution:

    def maximumWealth(self, accounts: List[List[int]]) -> int:
        return max([sum(x) for x in accounts])
```

---------------------

# 2025-10-04 03:21: 3280. Convert Date to Binary (Easy) (time: 10m 42):

```python3
class Solution:

    def toBin(self, n):
        (div, mod) = divmod(n, 2)
        ret = str(mod)
        if div:
            ret = str(self.toBin(div)) + ret
        return ret

    def convertDateToBinary(self, date: str) -> str:
        return '-'.join((self.toBin(int(x)) for x in date.split('-')))
```

---------------------

# 2025-10-04 03:27: 3289. The Two Sneaky Numbers of Digitville (Easy) (time: 4m 1):

```python3
class Solution:

    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        return [x[0] for x in filter(lambda x: x[1] == 2, dict(Counter(nums)).items())]
```

---------------------

# 2025-10-04 03:33: 1684. Count the Number of Consistent Strings (Easy) (time: 3m 13):

```python3
class Solution:

    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        allowed = set(allowed)
        return len([word for word in words if all((x in allowed for x in word))])
```

---------------------

# 2025-10-04 03:40: 3512. Minimum Operations to Make Array Sum Divisible by K (Easy) (time: 3m 41):

```python3
class Solution:

    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(nums) % k
```

---------------------

# 2025-10-04 03:47: 2413. Smallest Even Multiple (Easy) (time: 5m 22):

```python3
class Solution:

    def smallestEvenMultiple(self, n: int) -> int:
        i = 1
        while True:
            if i % 2 == 0 and i % n == 0:
                return i
            i += 1
```

---------------------

# 2025-10-04 04:00: 1678. Goal Parser Interpretation (Easy) (time: 4m 54):

```python3
class Solution:

    def interpret(self, command: str) -> str:
        return command.replace('(al)', 'al').replace('()', 'o')
```

---------------------

# 2025-10-04 04:15: 3498. Reverse Degree of a String (Easy) (time: 11m 18):

```python3
class Solution:

    def reverseDegree(self, s: str) -> int:
        res = 0
        for (i, c) in enumerate(s):
            reverse_pos = 27 - (ord(c) - 97 + 1)
            res += reverse_pos * (i + 1)
        return res
```

---------------------

# 2025-10-04 04:23: 2235. Add Two Integers (Easy) (time: 2m 35):

```python3
class Solution:

    def sum(self, num1: int, num2: int) -> int:
        return add(num1, num2)
```

---------------------

# 2025-10-05 05:42: 169. Majority Element (Easy) (time: 10m 39):

```python3
class Solution:

    def majorityElement(self, nums: List[int]) -> int:
        guess = nums[0]
        count = 1
        for i in range(1, len(nums)):
            if count == 0:
                guess = nums[i]
                count = 1
            elif nums[i] == guess:
                count += 1
            else:
                count -= 1
        return guess
```

---------------------

# 2025-10-05 05:55: 2220. Minimum Bit Flips to Convert Number (Easy) (time: 4m 33):

```python3
class Solution:

    def minBitFlips(self, start: int, goal: int) -> int:
        count = 0
        while start or goal:
            count += start & 1 != goal & 1
            start >>= 1
            goal >>= 1
        return count
```

---------------------

# 2025-10-05 06:01: 2798. Number of Employees Who Met the Target (Easy) (time: 1m 56):

```python3
class Solution:

    def numberOfEmployeesWhoMetTarget(self, hours: List[int], target: int) -> int:
        return sum([x >= target for x in hours])
```

---------------------

# 2025-10-05 06:08: 2574. Left and Right Sum Differences (Easy) (time: 3m 32):

```python3
class Solution:

    def leftRightDifference(self, nums: List[int]) -> List[int]:
        right_sum = accumulate(nums)
        left_sum = reversed([*accumulate(reversed(nums))])
        return [abs(a - b) for (a, b) in zip(right_sum, left_sum)]
```

---------------------

# 2025-10-05 06:13: 2824. Count Pairs Whose Sum is Less than Target (Easy) (time: 2m 25):

```python3
class Solution:

    def countPairs(self, nums: List[int], target: int) -> int:
        return sum((nums[i] + nums[j] < target for (i, j) in combinations(range(len(nums)), 2)))
```

---------------------

# 2025-10-05 06:18: 3146. Permutation Difference between Two Strings (Easy) (time: 3m 40):

```python3
class Solution:

    def findPermutationDifference(self, s: str, t: str) -> int:
        pos = {v: i for (i, v) in enumerate(t)}
        return sum((abs(i - pos[v]) for (i, v) in enumerate(s)))
```

---------------------

# 2025-10-05 06:34: 2037. Minimum Number of Moves to Seat Everyone (Easy) (time: 12m 40):

```python3
class Solution:

    def minMovesToSeat(self, seats: List[int], students: List[int]) -> int:
        return sum((abs(a - b) for (a, b) in zip(sorted(seats), sorted(students))))
```

## notes: 

Super confusing questions.

seats = [3,1,5]
students = [2,7,4]

I guess sorting might help:

seats = [1,3,5]
students = [2,4,7]

---------------------

# 2025-10-05 09:20: 1365. How Many Numbers Are Smaller Than the Current Number (Easy) (time: 7m 51):

```python3
class Solution:

    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        res = []
        for i in range(len(nums)):
            count = 0
            for j in range(len(nums)):
                if i != j:
                    if nums[j] < nums[i]:
                        count += 1
            res.append(count)
        return res
```

---------------------

# 2025-10-05 09:26: 1486. XOR Operation in an Array (Easy) (time: 4m 1):

```python3
class Solution:

    def xorOperation(self, n: int, start: int) -> int:
        return reduce(xor, [start + 2 * i for i in range(n)], 0)
```

---------------------

# 2025-10-05 10:07: 1720. Decode XORed Array (Easy) (time: 11m 7):

```python3
class Solution:

    def decode(self, encoded: List[int], first: int) -> List[int]:
        res = [first]
        for e in encoded:
            first ^= e
            res.append(first)
        return res
```

## notes: 

Kind of struggling to understand the question.

Input: encoded = [1,2,3], first = 1
Output: [1,0,2,1]
Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]

>>> 1 ^ 1
0
>>> 0 ^ 2
2
>>> 2 ^ 3

So it seems i simply need to xor start with the first encoded item,
then xor the result with the following items in 'encoded' successively.

---------------------

# 2025-10-05 10:17: 1603. Design Parking System (Easy) (time: 5m 0):

```python3
class CarSize:
    big = 1
    medium = 2
    small = 3

class ParkingSystem:

    def __init__(self, big: int, medium: int, small: int):
        self.spaces = {CarSize.big: big, CarSize.medium: medium, CarSize.small: small}

    def addCar(self, carType: int) -> bool:
        if self.spaces[carType] > 0:
            self.spaces[carType] -= 1
            return True
        else:
            return False
```

---------------------

# 2025-10-05 10:26: 1637. Widest Vertical Area Between Two Points Containing No Points (Easy) (time: 6m 4):

```python3
class Solution:

    def maxWidthOfVerticalArea(self, points: List[List[int]]) -> int:
        return max((b - a for (a, b) in pairwise((x[0] for x in sorted(points, key=lambda x: x[0])))))
```

---------------------

# 2025-10-05 10:50: 3264. Final Array State After K Multiplication Operations I (Easy) (time: 15m 44):

```python3
class Solution:

    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        for i in range(k):
            _min = min(nums)
            index = nums.index(_min)
            nums[index] *= multiplier
        return nums
```

---------------------

# 2025-10-05 11:00: 1791. Find Center of Star Graph (Easy) (time: 6m 5):

```python3
class Solution:

    def findCenter(self, edges: List[List[int]]) -> int:
        s = set(edges[0])
        for i in range(1, len(edges)):
            s.intersection_update(edges[i])
        return next(iter(s))
```

---------------------

# 2025-10-06 07:41: 2114. Maximum Number of Words Found in Sentences (Easy) (time: 1m 12):

```python3
class Solution:

    def mostWordsFound(self, sentences: List[str]) -> int:
        return max([len(x.split()) for x in sentences])
```

---------------------

# 2025-10-06 07:46: 1281. Subtract the Product and Sum of Digits of an Integer (Easy) (time: 2m 33):

```python3
class Solution:

    def subtractProductAndSum(self, n: int) -> int:

        def get_digits(n):
            digits = []
            while n:
                digits.append(n % 10)
                n //= 10
            return digits
        digits = get_digits(n)
        return prod(digits) - sum(digits)
```

---------------------

# 2025-10-06 07:57: 2000. Reverse Prefix of Word (Easy) (time: 9m 1):

```python3
class Solution:

    def reversePrefix(self, word: str, ch: str) -> str:
        if ch in word:
            index = word.index(ch)
            a = word[:index + 1][::-1]
            b = word[index + 1:]
            return a + b
        return word
```

---------------------

# 2025-10-06 08:06: 3285. Find Indices of Stable Mountains (Easy) (time: 4m 38):

```python3
class Solution:

    def stableMountains(self, height: List[int], threshold: int) -> List[int]:
        res = []
        for i in range(1, len(height)):
            if height[i - 1] > threshold:
                res.append(i)
        return res
```

---------------------

# 2025-10-06 08:19: 1021. Remove Outermost Parentheses (Easy) (time: 9m 55):

```python3
class Solution:

    def removeOuterParentheses(self, s: str) -> str:
        count = 0
        res = []
        current = ''
        start = False
        for c in s:
            if c == '(':
                if count == 0:
                    count += 1
                    start = True
                    continue
                count += 1
            else:
                count -= 1
                if count == 0:
                    start = False
                    res.append(current)
                    current = ''
            if start:
                current += c
        return ''.join(res)
```

---------------------

# 2025-10-06 08:28: 1389. Create Target Array in the Given Order (Easy) (time: 5m 59):

```python3
class Solution:

    def createTargetArray(self, nums: List[int], index: List[int]) -> List[int]:
        target = []
        for i in range(len(nums)):
            ind = index[i]
            num = nums[i]
            target.insert(ind, num)
        return target
```

---------------------

# 2025-10-06 08:35: 3065. Minimum Operations to Exceed Threshold Value I (Easy) (time: 0m 52):

```python3
class Solution:

    def minOperations(self, nums: List[int], k: int) -> int:
        return len([x for x in nums if x < k])
```

---------------------

# 2025-10-06 08:38: 1816. Truncate Sentence (Easy) (time: 0m 53):

```python3
class Solution:

    def truncateSentence(self, s: str, k: int) -> str:
        return ' '.join(s.split()[:k])
```

---------------------

# 2025-10-06 08:43: 1688. Count of Matches in Tournament (Easy) (time: 3m 5):

```python3
class Solution:

    def numberOfMatches(self, n: int) -> int:
        matches_played = 0
        while n != 1:
            if n % 2 == 0:
                matches = n // 2
                advance = n // 2
                n = advance
                matches_played += matches
            else:
                matches = (n - 1) // 2
                advance = (n - 1) // 2 + 1
                n = advance
                matches_played += matches
        return matches_played
```

---------------------

# 2025-10-06 08:57: 2160. Minimum Sum of Four Digit Number After Splitting Digits (Easy) (time: 3m 31):

```python3
class Solution:

    def minimumSum(self, num: int) -> int:
        nums = list(str(num))
        nums.sort()
        a = nums[0] + nums[2]
        b = nums[1] + nums[3]
        return int(a) + int(b)
```

---------------------

# 2025-10-06 09:03: 1313. Decompress Run-Length Encoded List (Easy) (time: 3m 22):

```python3
class Solution:

    def decompressRLElist(self, nums: List[int]) -> List[int]:
        res = []
        for i in range(0, len(nums), 2):
            res.extend([nums[i + 1]] * nums[i])
        return res
```

---------------------

# 2025-10-07 05:20: 3162. Find the Number of Good Pairs I (Easy) (time: 5m 0):

```python3
class Solution:

    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        count = 0
        for i in range(len(nums1)):
            for j in range(len(nums2)):
                if nums1[i] % (nums2[j] * k) == 0:
                    count += 1
        return count
```

## notes: 

The 5 good pairs are (0, 0), (1, 0), (1, 1), (2, 0), and (2, 2).

---------------------

# 2025-10-07 05:28: 1662. Check If Two String Arrays are Equivalent (Easy) (time: 2m 53):

```python3
class Solution:

    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        return all((a == b for (a, b) in zip_longest(chain(*word1), chain(*word2))))
```

---------------------

# 2025-10-07 05:57: 2859. Sum of Values at Indices With K Set Bits (Easy) (time: 7m 16):

```python3
class Solution:

    def count_bits(self, n):
        count = 0
        while n:
            count += 1
            n &= n - 1
        return count

    def sumIndicesWithKSetBits(self, nums: List[int], k: int) -> int:
        count = 0
        for (i, n) in enumerate(nums):
            bits = self.count_bits(i)
            if bits == k:
                count += n
        return count
```

---------------------

# 2025-10-07 06:04: 2520. Count the Digits That Divide a Number (Easy) (time: 3m 33):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def countDigits(self, num: int) -> int:
        res = 0
        counts = dict(Counter(self.getDigits(num))).items()
        for (k, v) in counts:
            if num % k == 0:
                res += v
        return res
```

---------------------

# 2025-10-07 06:13: 1379. Find a Corresponding Node of a Binary Tree in a Clone of That Tree (Easy) (time: 4m 16):

```python3
class Solution:

    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:

        def dfs(node):
            if not node:
                return
            if node.val == target.val:
                return node
            return dfs(node.left) or dfs(node.right)
        return dfs(cloned)
```

---------------------

# 2025-10-07 06:22: 1342. Number of Steps to Reduce a Number to Zero (Easy) (time: 1m 18):

```python3
class Solution:

    def numberOfSteps(self, num: int) -> int:
        steps = 0
        while num:
            steps += 1
            if num % 2 == 0:
                num //= 2
            else:
                num -= 1
        return steps
```

---------------------

# 2025-10-07 08:07: 2652. Sum Multiples (Easy) (time: 3m 15):

```python3
class Solution:

    def sumOfMultiples(self, n: int) -> int:
        return sum((x for x in range(1, n + 1) if x % 3 == 0 or x % 5 == 0 or x % 7 == 0))
```

---------------------

# 2025-10-07 08:16: 3427. Sum of Variable Length Subarrays (Easy) (time: 3m 26):

```python3
class Solution:

    def subarraySum(self, nums: List[int]) -> int:
        res = 0
        for i in range(len(nums)):
            start = max(0, i - nums[i])
            res += sum(nums[start:i + 1])
        return res
```

---------------------

# 2025-10-07 08:22: 2367. Number of Arithmetic Triplets (Easy) (time: 0m 40):

```python3
class Solution:

    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        triplets = 0
        for (i, j, k) in combinations(range(len(nums)), 3):
            if nums[j] - nums[i] == diff and nums[k] - nums[j] == diff:
                triplets += 1
        return triplets
```

---------------------

# 2025-10-07 08:27: 2535. Difference Between Element Sum and Digit Sum of an Array (Easy) (time: 2m 19):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def differenceOfSum(self, nums: List[int]) -> int:
        _sum = sum(nums)
        digit_sum = sum(chain(*[self.getDigits(x) for x in nums]))
        return abs(_sum - digit_sum)
```

---------------------

# 2025-10-07 08:31: 2974. Minimum Number Game (Easy) (time: 0m 35):

```python3
class Solution:

    def numberGame(self, nums: List[int]) -> List[int]:
        arr = []
        while nums:
            alice_min = min(nums)
            nums.remove(alice_min)
            bob_min = min(nums)
            nums.remove(bob_min)
            arr.extend([bob_min, alice_min])
        return arr
```

---------------------

# 2025-10-07 08:39: 1773. Count Items Matching a Rule (Easy) (time: 1m 52):

```python3
class Rule:
    type = 0
    color = 1
    name = 2

class Solution:

    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        matches = 0
        for item in items:
            rule_one_matches = ruleKey == 'type' and ruleValue == item[Rule.type]
            rule_two_matches = ruleKey == 'color' and ruleValue == item[Rule.color]
            rule_three_matches = ruleKey == 'name' and ruleValue == item[Rule.name]
            if rule_one_matches or rule_two_matches or rule_three_matches:
                matches += 1
        return matches
```

---------------------

# 2025-10-07 08:51: 3194. Minimum Average of Smallest and Largest Elements (Easy) (time: 1m 30):

```python3
class Solution:

    def minimumAverage(self, nums: List[int]) -> float:
        averages = []
        for _ in range(len(nums) // 2):
            _min = min(nums)
            nums.remove(_min)
            _max = max(nums)
            nums.remove(_max)
            averages.append((_min + _max) / 2)
        return min(averages)
```

---------------------

# 2025-10-07 08:55: 2236. Root Equals Sum of Children (Easy) (time: 0m 48):

```python3
class Solution:

    def checkTree(self, root: Optional[TreeNode]) -> bool:
        return root.val == root.left.val + root.right.val
```

---------------------

# 2025-10-07 09:16: 1614. Maximum Nesting Depth of the Parentheses (Easy) (time: 5m 4):

```python3
class Solution:

    def maxDepth(self, s: str) -> int:
        count = 0
        depth = 0
        for c in s:
            if c == '(':
                count += 1
            elif c == ')':
                count -= 1
            depth = max(depth, count)
        return depth
```

---------------------

# 2025-10-07 09:19: 2185. Counting Words With a Given Prefix (Easy) (time: 1m 28):

```python3
class Solution:

    def prefixCount(self, words: List[str], pref: str) -> int:
        return sum((x.startswith(pref) for x in words))
```

---------------------

# 2025-10-07 09:24: 2418. Sort the People (Easy) (time: 4m 39):

```python3
class Solution:

    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        enum = [*enumerate(names)]
        enum.sort(key=lambda x: heights[x[0]])
        return [x[1] for x in enum][::-1]
```

---------------------

# 2025-10-07 09:47: 3300. Minimum Element After Replacement With Digit Sum (Easy) (time: 1m 2):

```python3
class Solution:

    def addDigitsUntil1Digit(self, num):
        num = sum((int(x) for x in str(num)))
        return num

    def minElement(self, nums: List[int]) -> int:
        return min((self.addDigitsUntil1Digit(x) for x in nums))
```

---------------------

# 2025-10-07 11:25: 2956. Find Common Elements Between Two Arrays (Easy) (time: 7m 14):

```python3
class Solution:

    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        left = 0
        for i in range(len(nums1)):
            if nums1[i] in nums2:
                left += 1
        right = 0
        for i in range(len(nums2)):
            if nums2[i] in nums1:
                right += 1
        return [left, right]
```

---------------------

# 2025-10-07 11:59: 2194. Cells in a Range on an Excel Sheet (Easy) (time: 8m 59):

```python3
class Solution:

    def cellsInRange(self, s: str) -> List[str]:
        (start_col, start_row, _, end_col, end_row) = list(s)
        start_col_index = ascii_uppercase.index(start_col)
        end_col_index = ascii_uppercase.index(end_col)
        letters = ascii_uppercase[start_col_index:end_col_index + 1]
        numbers = list(range(int(start_row), int(end_row) + 1))
        res = [*product(letters, numbers)]
        return [''.join((str(y) for y in x)) for x in res]
```

---------------------

# 2025-10-07 12:09: 557. Reverse Words in a String III (Easy) (time: 2m 12):

```python3
class Solution:

    def reverseWords(self, s: str) -> str:
        return ' '.join((x[::-1] for x in s.split()))
```

---------------------

# 2025-10-07 12:13: 1832. Check if the Sentence Is Pangram (Easy) (time: 9m 25):

```python3
class Solution:

    def checkIfPangram(self, sentence: str) -> bool:
        counter = Counter(sentence)
        return all((counter.get(c, 0) >= 1 for c in ascii_lowercase))
```

---------------------

# 2025-10-07 12:18: 2108. Find First Palindromic String in the Array (Easy) (time: 2m 20):

```python3
class Solution:

    def firstPalindrome(self, words: List[str]) -> str:
        return next((x for x in words if x == x[::-1]), '')
```

---------------------

# 2025-10-07 12:24: 3099. Harshad Number (Easy) (time: 19m 39):

```python3
class Solution:

    def sumOfTheDigitsOfHarshadNumber(self, x: int) -> int:
        harshad = lambda x: sum((int(y) for y in str(x)))
        is_harshad = lambda x, h: x % h == 0
        h = harshad(x)
        return h if is_harshad(x, h) else -1
```

---------------------

# 2025-10-07 12:31: 1859. Sorting the Sentence (Easy) (time: 6m 35):

```python3
class Solution:

    def sortSentence(self, s: str) -> str:
        p = '(\\w+)(\\d+)'
        words = [match(p, word).groups() for word in s.split()]
        words.sort(key=lambda x: x[1])
        return ' '.join((x[0] for x in words))
```

---------------------

# 2025-10-07 13:23: 1464. Maximum Product of Two Elements in an Array (Easy) (time: 2m 9):

```python3
class Solution:

    def maxProduct(self, nums: List[int]) -> int:
        return max(((nums[i] - 1) * (nums[j] - 1) for (i, j) in combinations(range(len(nums)), 2)))
```

---------------------

# 2025-10-07 13:31: 1475. Final Prices With a Special Discount in a Shop (Easy) (time: 8m 19):

```python3
class Solution:

    def finalPrices(self, prices: List[int]) -> List[int]:
        res = []
        for (i, p) in enumerate(prices):
            disc = next(filter(lambda x: x <= p, prices[i + 1:]), None)
            res.append(p - disc if disc is not None else p)
        return res
```

---------------------

# 2025-10-07 13:38: 2485. Find the Pivot Integer (Easy) (time: 6m 0):

```python3
class Solution:

    def pivotInteger(self, n: int) -> int:
        s = sum(range(1, n + 1))
        t = 0
        for i in range(1, n + 1):
            s -= i
            if t == s:
                return i
            t += i
        return -1
```

---------------------

# 2025-10-07 13:47: 804. Unique Morse Code Words (Easy) (time: 8m 6):

```python3
class Solution:

    def uniqueMorseRepresentations(self, words: List[str]) -> int:
        morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
        code = {l: morse[i] for (i, l) in enumerate(ascii_lowercase)}
        return len(set([''.join((code[c] for c in word)) for word in words]))
```

## notes: 

","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]

Given an array of strings words where each word can be written as a concatenation of the Morse code of each letter.

    For example, "cab" can be written as "-.-..--...", which is the concatenation of "-.-.", ".-", and "-...". We will call such a concatenation the transformation of a word.

Return the number of different transformations among all words we have.

Example 1:

Input: words = ["gin","zen","gig","msg"]
Output: 2
Explanation: The transformation of each word is:
"gin" -> "--...-."
"zen" -> "--...-."
"gig" -> "--...--."
"msg" -> "--...--."
There are 2 different transformations: "--...-." and "--...--.".

Example 2:

Input: words = ["a"]
Output: 1

Constraints:

    1 <= words.length <= 100
    1 <= words[i].length <= 12
    words[i] consists of lowercase English letters.

---------------------

# 2025-10-07 14:07: 1588. Sum of All Odd Length Subarrays (Easy) (time: 17m 42):

```python3
class Solution:

    def sumOddLengthSubarrays(self, arr: List[int]) -> int:
        count = 0
        for i in range(1, len(arr) + 1, 2):
            for j in range(len(arr)):
                if i + j > len(arr):
                    break
                sub = arr[j:j + i]
                count += sum(sub)
        return count
```

## notes: 

Had a think a little bit more for this problem. This definitely
feels like a brute force solution.

---------------------

# 2025-10-07 15:04: 2315. Count Asterisks (Easy) (time: 5m 24):

```python3
class Solution:

    def countAsterisks(self, s: str) -> int:
        s = s.split('|')
        count = 0
        for c in range(0, len(s), 2):
            count += s[c].count('*')
        return count
```

---------------------

# 2025-10-07 15:06: 2828. Check if a String Is an Acronym of Words (Easy) (time: 1m 24):

```python3
class Solution:

    def isAcronym(self, words: List[str], s: str) -> bool:
        accro = ''.join((a[0] for a in words))
        return accro == s
```

---------------------

# 2025-10-07 15:18: 1913. Maximum Product Difference Between Two Pairs (Easy) (time: 12m 10):

```python3
class Solution:

    def maxProductDifferenceBruteForce(self, nums: List[int]) -> int:
        return max((a * b - c * d for (a, b, c, d) in permutations(nums, 4)))

    def maxProductDifference(self, nums: List[int]) -> int:
        nums.sort()
        n = nums
        return n[-1] * n[-2] - n[0] * n[1]
```

## notes: 

brute force permutations works, but hits TLE. Need more optimal approach.

[5, 6, 2, 7, 4]

since we want to maximize the result, we should pick the largest values for a and b,
and the smallest for c and d.

---------------------

# 2025-10-07 15:25: 1935. Maximum Number of Words You Can Type (Easy) (time: 28m 4):

```python3
class Solution:

    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        b = set(brokenLetters)
        t = [set(w) for w in text.split(' ')]
        count = len(t)
        for w in t:
            if w.intersection(b):
                count -= 1
        return count
```

---------------------

# 2025-10-07 15:48: 2864. Maximum Odd Binary Number (Easy) (time: 21m 42):

```python3
class Solution:

    def maximumOddBinaryNumber(self, s: str) -> str:
        ones = s.count('1')
        zeros = len(s) - ones
        return '1' * (ones - 1) + '0' * zeros + '1'
```

## notes: 

Interesting problem. I'm thinking of just computing the maximum value possible for the given bits,
then interating backwards until i get an odd number.

---------------------

# 2025-10-07 17:02: 2423. Remove Letter To Equalize Frequency (Easy) (time: 50m 56):

```python3
class Solution:

    def equalFrequency(self, word: str) -> bool:
        for i in range(len(word)):
            sub = word[:i] + word[i + 1:]
            freq = list(dict(Counter(sub)).values())
            if len(set(freq)) == 1:
                return True
        return False
```

## notes: 

Wow this question is hard. So we have to delete one character, and we need to return whether all letter frequencies will
be the same. Somehow i think a counter is needed.

'abc' -> [1, 1, 1] # True - covered

So we have a list where all counts are 1, and the same.. so this case works because we can delete one element and keep
the counts the same.

'abac' -> [2, 1, 1] # True

This also works, because we can delete one 'a' to get [1, 1, 1]

'bccc' -> [1, 3] # True - covered

This also works, because we can delete the odd one out ('b') and get similar counts.

'bcccddd' -> [1, 3, 3] # True - covered

This also works, because we can delete the odd one out ('b') and get similar counts.

'aazz' -> [2, 2] # False - covered

This on the other hand doesn't work, because all frequencies are similar, so deleting one character would
throw off our numbers.

'aaabbbccc' -> [3, 3, 3] # False - covered

Same thing! So i'm spotting a trend. If all frequencies are the same, and greater than 1, it's false
because changing one frequency would result in non equal frequencies.

Hmm nvm the solution was brute force.

---------------------

# 2025-10-08 05:15: 3502. Minimum Cost to Reach Every Position (Easy) (time: 5m 34):

```python3
class Solution:

    def minCosts(self, cost: List[int]) -> List[int]:
        res = [0] * len(cost)
        _min = float('inf')
        for (i, c) in enumerate(cost):
            _min = min(c, _min)
            res[i] = _min
        return res
```

## notes: 

This question is poorly worded. Anyway hints at computing the minimum prefix array

---------------------

# 2025-10-08 05:20: 1967. Number of Strings That Appear as Substrings in Word (Easy) (time: 2m 41):

```python3
class Solution:

    def numOfStrings(self, patterns: List[str], word: str) -> int:
        res = 0
        for pattern in patterns:
            res += pattern in word
        return res
```

---------------------

# 2025-10-08 05:28: 1290. Convert Binary Number in a Linked List to Integer (Easy) (time: 8m 0):

```python3
class Solution:

    def getDecimalValue(self, head: ListNode) -> int:
        it = head
        st = ''
        while it:
            st += '1' if it.val else '0'
            it = it.next
        return int(st, base=2)
```

## notes: 

Wondering if this can be done in O(1) extra space

1         0         1
2^2 * 1   2^1 * 0   2^0 * 1
4         0         1

Hmm might just built up a string.

---------------------

# 2025-10-08 05:37: 2053. Kth Distinct String in an Array (Easy) (time: 6m 6):

```python3
class Solution:

    def kthDistinct(self, arr: List[str], k: int) -> str:
        vals = [s for (s, count) in dict(Counter(arr)).items() if count == 1]
        return vals[k - 1] if k - 1 < len(vals) else ''
```

---------------------

# 2025-10-08 05:44: 1266. Minimum Time Visiting All Points (Easy) (time: 6m 54):

```python3
class Solution:

    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        return reduce(lambda acc, P: acc + max(abs(P[1][0] - P[0][0]), abs(P[1][1] - P[0][1])), pairwise(points), 0)
```

---------------------

# 2025-10-08 05:50: 1844. Replace All Digits with Characters (Easy) (time: 4m 32):

```python3
class Solution:

    def shift(self, c, x):
        return chr(ord(c) + x)

    def replaceDigits(self, s: str) -> str:
        s = list(s)
        for i in range(1, len(s), 2):
            s[i] = self.shift(s[i - 1], int(s[i]))
        return ''.join(s)
```

---------------------

# 2025-10-08 06:00: 3683. Earliest Time to Finish One Task (Easy) (time: 3m 22):

```python3
class Solution:

    def earliestTime(self, tasks: List[List[int]]) -> int:
        return min((ti + si for (si, ti) in tasks))
```

---------------------

# 2025-10-08 06:30: 2331. Evaluate Boolean Binary Tree (Easy) (time: 7m 37):

```python3
from operator import or_, and_

class Solution:

    def evaluateTree(self, root: Optional[TreeNode]) -> bool:

        def dfs(node):
            is_leaf = node.left is None and node.right is None
            if is_leaf:
                return bool(node.val)
            left = dfs(node.left)
            right = dfs(node.right)
            return ops[node.val](left, right)
        ops = {2: or_, 3: and_}
        return dfs(root) if root else False
```

---------------------

# 2025-10-08 07:43: 3131. Find the Integer Added to Array I (Easy) (time: 7m 24):

```python3
class Solution:

    def addedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        x = min(nums2) - min(nums1)
        return x
```

---------------------

# 2025-10-08 07:51: 724. Find Pivot Index (Easy) (time: 3m 21):

```python3
class Solution:

    def pivotIndex(self, nums: List[int]) -> int:
        left = 0
        right = sum(nums)
        for (i, v) in enumerate(nums):
            right -= v
            if left == right:
                return i
            left += v
        return -1
```

---------------------

# 2025-10-08 08:17: 19. Remove Nth Node From End of List (Medium) (time: 14m 58):

```python3
class Solution:

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        it = head
        dummy = ListNode()
        dummy.next = head
        trailing = dummy
        i = 0
        while it:
            if i >= n:
                trailing = trailing.next
            it = it.next
            i += 1
        if trailing:
            trailing.next = trailing.next.next if trailing.next else None
        return dummy.next
```

## notes: 

OK so we'll need to iterate until the end of the list, and maintain a back
pointer, so it points to end -n.

---------------------

# 2025-10-08 08:54: 238. Product of Array Except Self (Medium) (time: 15m 38):

```python3
from operator import mul

class Solution:

    def productExceptSelfLetters(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x)]
        left = ['1'] + acc(nums[:-1])
        right = (['1'] + acc(nums[1:][::-1]))[::-1]
        return [a + b for (a, b) in zip(left, right)]

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x, mul)]
        left = [1] + acc(nums[:-1])
        right = ([1] + acc(nums[1:][::-1]))[::-1]
        return [a * b for (a, b) in zip(left, right)]
```

## notes: 

OK so with this problem, it really helps to use variables instead of numbers, and think in terms
of output.

So with [a, b, c, d], the output is:

bcd, acd, abd, abc

so accumulating from the left, we get:

1, a, ab, abc

accumulating from the right, we get:

dcb dc d  1

multiplying these two gives us:

bcd, acd, abd, abc

---------------------

# 2025-10-08 09:42: 617. Merge Two Binary Trees (Easy) (time: 12m 45):

```python3
class Solution:

    def mergeTrees(self, t1: Optional[TreeNode], t2: Optional[TreeNode]) -> Optional[TreeNode]:

        def dfs(a, b):
            if a is None and b is None:
                return
            if a and b:
                return TreeNode(a.val + b.val, dfs(a.left, b.left), dfs(a.right, b.right))
            else:
                c = a or b
                return TreeNode(c.val, dfs(a.left if a else None, b.left if b else None), dfs(a.right if a else None, b.right if b else None))
        return dfs(t1, t2)
```

---------------------

# 2025-10-08 10:01: 102. Binary Tree Level Order Traversal (Medium) (time: 6m 38):

```python3
class Solution:

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        def dfs(node, depth=0):
            if not node:
                return
            levels[depth].append(node.val)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)
        levels = defaultdict(list)
        dfs(root)
        return [x[1] for x in sorted(levels.items(), key=lambda x: x[0])]
```

---------------------

# 2025-10-08 11:15: 209. Minimum Size Subarray Sum (Medium) (time: 50m 21):

```python3
class Solution:

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        prefix = [*accumulate(nums)] + [0]
        range_sum = lambda i, j: prefix[j] - prefix[i - 1]
        (i, j) = (0, 0)
        min_size = float('inf')
        while j < len(nums):
            _sum = range_sum(i, j)
            if _sum < target:
                j += 1
            elif _sum > target:
                min_size = min(min_size, j - i + 1)
                i += 1
            else:
                min_size = min(min_size, j - i + 1)
                i += 1
        return min_size if min_size != float('inf') else 0
```

## notes: 

Let's begin with subarray sum equals k. I was very close to remembering it
Useful warmup.

Now to this problem. It seems the main thing that might help here is the
ability to get the sum between i and j, which we can do with a prefix array.

Then a sliding window which grows and shrinks to find subarrays gte to the target.
Then track the min size of the window.

Solved.

---------------------

# 2025-10-08 11:29: 485. Max Consecutive Ones (Easy) (time: 3m 20):

```python3
class Solution:

    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        consecutive = 0
        max_ones = 0
        for n in nums:
            if n:
                consecutive += 1
                max_ones = max(max_ones, consecutive)
            else:
                consecutive = 0
        return max_ones
```

---------------------

# 2025-10-09 04:30: 287. Find the Duplicate Number (Medium) - learning (time: 30m 9):

```python3
class Solution(object):

    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

## notes: 

Didn't figure out the key insight that values can be used as
indices themselves, turning this into a cycle detection algorithm.

---------------------

# 2025-10-09 05:17: 142. Linked List Cycle II (Medium) (time: 20m 30):

```python3
class Solution:

    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return
        (slow, fast) = (head, head)
        has_cycle = False
        while slow and fast and slow.next and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                has_cycle = True
                break
        if not has_cycle:
            return
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow
```

## notes: 

- Slow and fast pointers start on head
- Slow iterates by 1, Fast by 2
- When they meet, set slow to head
- Iterate them together until they meet

---------------------

# 2025-10-09 05:57: 2. Add Two Numbers (Medium) (time: 22m 3):

```python3
class Solution:

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        carry = 0
        it = dummy
        while l1 or l2 or carry:
            val = carry
            if l1:
                val += l1.val
                l1 = l1.next
            if l2:
                val += l2.val
                l2 = l2.next
            (carry, mod) = divmod(val, 10)
            it.next = ListNode(mod)
            it = it.next
        return dummy.next
```

## notes: 

Create the dummy head of a new list.
Create two it pointers for each list.
While there's an it pointer that's still valid and there's no carry.
Add both pointer values. divmod.
Create new list node, and connect previous to this node.
Set remaining to node
set carry to div.

---------------------

# 2025-10-09 06:28: 83. Remove Duplicates from Sorted List (Easy) (time: 7m 41):

```python3
class Solution:

    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dh = ListNode()
        dh.next = head
        it = head
        while it and it.next:
            if it.next.val == it.val:
                it.next = it.next.next
            else:
                it = it.next
        return dh.next
```

---------------------

# 2025-10-09 07:25: 24. Swap Nodes in Pairs (Medium) - learning:

```python3
class Solution:

    def swapPairs(self, head: ListNode) -> ListNode:
        if head:
            h = head.next
            if h:
                (h.next, head.next) = (head, h.next)
                h.next.next = self.swapPairs(h.next.next)
                return h
        return head
```

## notes: 

Could only get it to work with an odd number of nodes.
Looked up a recursive solution. It's neat.

---------------------

# 2025-10-09 08:41: 328. Odd Even Linked List (Medium) (time: 11m 17):

```python3
class Solution:

    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return
        do = ListNode('dh', head)
        de = ListNode('de', head.next)
        a = head
        b = head.next
        while a and b and b.next:
            a.next = b.next
            b.next = b.next.next
            a = a.next
            b = b.next
        a.next = de.next
        return do.next
```

---------------------

# 2025-10-09 09:06: 82. Remove Duplicates from Sorted List II (Medium) - learning (time: 15m 8):

```python3
class Solution:

    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
```

## notes: 

Started solving the wrong question. Didn't realise duplicates had to go
entirely. Will revisit later.

---------------------

# 2025-10-09 09:14: 344. Reverse String (Easy) (time: 1m 36):

```python3
from typing import List

class Solution:

    def reverseString(self, s: List[str]) -> None:
        for i in range(len(s) // 2):
            (s[i], s[~i]) = (s[~i], s[i])
```

---------------------

# 2025-10-09 09:33: 160. Intersection of Two Linked Lists (Easy) (time: 10m 0):

```python3
class Solution:

    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:

        def listLength(head):
            count = 0
            while head:
                count += 1
                head = head.next
            return count
        a_length = listLength(headA)
        b_length = listLength(headB)
        diff = abs(a_length - b_length)
        diff_it = (headB, headA)[a_length > b_length]
        for _ in range(diff):
            diff_it = diff_it.next
        if a_length > b_length:
            headA = diff_it
        else:
            headB = diff_it
        while headA != headB:
            headA = headA.next
            headB = headB.next
        return headA
```

## notes: 

Ok i'll try the follow up version.

Algo:

- get length of both lists, i.e n1 and n2
- calc diff, i.e 2
- advance longest list by diff
- iterate both lists until pointers meet

---------------------

# 2025-10-09 10:48: 92. Reverse Linked List II (Medium) - learning (time: 56m 28):

```python3
class Solution:

    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        cur = prev.next
        for _ in range(right - left):
            temp = cur.next
            cur.next = temp.next
            temp.next = prev.next
            prev.next = temp
        return dummy.next
```

## notes: 

Ran out of time.

Came up with a not so great solution, which passed some of the test cases.
Ran out of time, so looked at a solution.

The main insight that really annoyed me missing is that the node values are labelled
1, 2, 3, 4, 5 which means i can iterate using ranges, using left, right, right - left
etc.

Also I need more practice reversing a linked list.

---------------------

# 2025-10-09 14:43: 206. Reverse Linked List (Easy) - learning (time: 10m 56):

```python3
class Solution:

    def reverseList(self, h: Optional[ListNode]) -> Optional[ListNode]:
        d = ListNode(0)
        while h:
            (d.next, h.next, h) = (h, d.next, h.next)
        return d.next
```

## notes: 

Ok so this is the best iterative alg, IMO. It's not my solution, i'm just learning here.
We start with a dummy head, not pointing to head. We iterate as long as head is valid.
We use tuple unpacking and perform all the work in one go.

We start with the dummy.next first, and it'll get simultaneously assigned head.
Ultimately we'll return d.next. For now, it performs that first connection, of
making the dummy.next point to the head.

Then we simultaneously connect h.next to d.next, which sets it to None on our first
iteration.

Finally h becomes h.next, which we can really just think of as regular iterating of
an 'it' or 'curr' pointer.

---------------------

# 2025-10-09 15:55: 61. Rotate List (Medium) (time: 17m 33):

```python3
class Solution:

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return
        if not head:
            return []
        if not head.next:
            return head
        if k == 0:
            return head
        count = 0
        it = head
        while it:
            count += 1
            it = it.next
        shift_by = count - k % count
        if k % count == 0:
            return head
        it = head
        for _ in range(shift_by - 1):
            it = it.next
        cont = it.next
        if it:
            it.next = None
        new_head = cont
        while cont:
            if cont.next:
                cont = cont.next
            else:
                cont.next = head
                break
        return new_head
```

---------------------

# 2025-10-09 17:54: 143. Reorder List (Medium) (time: 26m 48):

```python3
class Solution:

    def reorderList(self, head: Optional[ListNode]) -> None:
        it = head
        length = 0
        while it:
            it = it.next
            length += 1
        it = head
        for _ in range(length // 2 + (-1 if length % 2 == 0 else 0)):
            it = it.next
        second_half = it.next
        it.next = None
        d = ListNode(-1)
        h = second_half
        while h:
            (d.next, h.next, h) = (h, d.next, h.next)
        second_half = d.next
        d.next = None
        it = d
        it1 = head
        it2 = second_half
        i = 0
        while it1 or it2:
            if i % 2 == 0 and it1:
                it.next = it1
                it = it1
                it1 = it1.next
            elif i % 2 != 0 and it2:
                it.next = it2
                it = it2
                it2 = it2.next
            else:
                it.next = (it1 or it2).next
                it = it1 or it2
                it1 = it1.next if it1 else None
                it2 = it2.next if it2 else None
            i += 1
        return d.next
```

---------------------

# 2025-10-10 04:38: 86. Partition List (Medium) (time: 28m 40):

```python3
class Solution:

    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        d = ListNode('dummy')
        d.next = head
        gt_head = ListNode('gt')
        gt_it = gt_head
        it = d
        while it.next:
            if it.next.val >= x:
                gt_it.next = it.next
                gt_it = gt_it.next
                it.next = it.next.next
                gt_it.next = None
            else:
                it = it.next
        it.next = gt_head.next
        return d.next
```

---------------------

# 2025-10-10 05:00: 237. Delete Node in a Linked List (Medium) (time: 11m 38):

```python3
class Solution:

    def deleteNode(self, node):
        last = None
        while node.next:
            if node.next.next is None:
                last = node
            node.val = node.next.val
            node = node.next
        last.next = None
```

---------------------

# 2025-10-10 05:21: 445. Add Two Numbers II (Medium) (time: 4m 3):

```python3
class Solution:

    def reverse(self, head):
        d = ListNode(-1)
        while head:
            (d.next, head.next, head) = (head, d.next, head.next)
        return d.next

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        l1 = self.reverse(l1)
        l2 = self.reverse(l2)
        dummy = ListNode()
        carry = 0
        it = dummy
        while l1 or l2 or carry:
            val = carry
            if l1:
                val += l1.val
                l1 = l1.next
            if l2:
                val += l2.val
                l2 = l2.next
            (carry, mod) = divmod(val, 10)
            it.next = ListNode(mod)
            it = it.next
        return self.reverse(dummy.next)
```

---------------------

# 2025-10-10 06:21: 25. Reverse Nodes in k-Group (Hard) (time: 42m 22):

```python3
class Solution:

    def reverse_sublist(self, h, n):
        d = ListNode(-1)
        t = h
        for _ in range(n):
            if not h:
                break
            (d.next, h.next, h) = (h, d.next, h.next)
        else:
            t.next = h
        return (d.next, t)

    def get_length(self, h, c=0):
        while h:
            (h, c) = (h.next, c + 1)
        return c

    def reverseKGroup(self, h: Optional[ListNode], k: int) -> Optional[ListNode]:
        it = d = ListNode(-1, h)
        n = self.get_length(h)
        for _ in range(n // k):
            (it.next, it) = self.reverse_sublist(it.next, k)
        return d.next
```

---------------------

# 2025-10-10 07:56: 701. Insert into a Binary Search Tree (Medium) (time: 21m 13):

```python3
class Solution:

    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:

        def dfs(node, parent):
            if not node:
                parent.left = TreeNode(val)
                return
            is_leaf = node.left is None and node.right is None
            if is_leaf:
                if val > node.val:
                    node.right = TreeNode(val)
                else:
                    node.left = TreeNode(val)
            elif val > node.val:
                if node.right:
                    dfs(node.right, node)
                else:
                    node.right = TreeNode(val)
            elif node.left:
                dfs(node.left, node)
            else:
                node.left = TreeNode(val)
        d = TreeNode(float('-inf'), root)
        dfs(d.left, d)
        return d.left
```

---------------------

# 2025-10-10 08:20: 268. Missing Number (Easy) (time: 15m 4):

```python3
class Solution:

    def missingNumber(self, nums: List[int]) -> int:
        return next(iter(list(set(range(len(nums) + 1)) - set(nums))))
```

## notes: 

Wasted some time thinking about the Follow up.

---------------------

# 2025-10-10 09:41: 349. Intersection of Two Arrays (Easy) (time: 1m 29):

```python3
class Solution:

    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1).intersection(nums2))
```

---------------------

# 2025-10-10 10:09: 941. Valid Mountain Array (Easy) - learning (time: 10m 11):

```python3
from typing import List

class Solution:

    def validMountainArray(self, arr: List[int]) -> bool:
        is_increasing = lambda i: arr[i - 1] < arr[i]
        is_decreasing = lambda i: arr[i - 1] > arr[i]
        is_peak = lambda i: i > 0 and is_increasing(i - 1) and is_decreasing(i + 1) and (i < len(arr))
```

## notes: 

941 is not an easy question. Easy tag is misleading,
so not great being told something is easy when it isn't.

Will revisit with the medium framing.

---------------------

# 2025-10-10 10:22: 189. Rotate Array (Medium) (time: 6m 11):

```python3
class Solution:

    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        if 0 < k < n:
            nums[:] = nums[n - k:] + nums[:n - k]
```

---------------------

# 2025-10-11 03:30: 704. Binary Search (Easy) (time: 4m 2):

```python3
class Solution:

    def search(self, nums: List[int], target: int) -> int:
        (left, right) = (0, len(nums) - 1)
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return -1
```

---------------------

# 2025-10-11 03:34: 35. Search Insert Position (Easy) (time: 0m 46):

```python3
class Solution:

    def searchInsert(self, nums: List[int], target: int) -> int:
        return bisect_left(nums, target)
```

---------------------

# 2025-10-11 03:53: 74. Search a 2D Matrix (Medium) (time: 16m 46):

```python3
class MatToList:

    def __init__(self, mat):
        self.mat = mat

    def __getitem__(self, i):
        (div, mod) = divmod(i, len(next(iter(self.mat), 0)))
        return self.mat[div][mod]

    def __len__(self):
        return len(self.mat) * len(next(iter(self.mat), []))

class Solution:

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        mat = MatToList(matrix)
        (left, right) = (0, len(mat) - 1)
        while left <= right:
            mid = (left + right) // 2
            val = mat[mid]
            if target == val:
                return True
            elif target < val:
                right = mid - 1
            else:
                left = mid + 1
        return False
```

---------------------

# 2025-10-11 05:06: 33. Search in Rotated Sorted Array (Medium) - learning (time: 55m 56):

```python3
class Solution:

    def search(self, nums: List[int], target: int) -> int:
        (left, right) = (0, len(nums) - 1)
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            left_is_sorted = nums[left] <= nums[mid]
            right_is_sorted = not left_is_sorted
            if left_is_sorted:
                target_is_in_left = nums[left] <= target < nums[mid]
                if target_is_in_left:
                    right = mid - 1
                else:
                    left = mid + 1
            elif right_is_sorted:
                target_is_in_right = nums[mid] < target <= nums[right]
                if target_is_in_right:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1
```

## notes: 

This question is my archnemesis for some reason. I got close, but had to
look up the solution in the end.

I don't know why. It's really not that hard. We can only search in sorted arrays
so if the left is sorted, our first decision is to branch into the left
search conditional, then if it's in the left, the next iteration will
search in this sublist, else it'll search the other.

Vice versa with the right side. I keep encountering this question, and
forgetting.

Will need to revisit soon.

---------------------

# 2025-10-11 05:43: 153. Find Minimum in Rotated Sorted Array (Medium) (time: 20m 39):

```python3
class Solution:

    def findMin(self, nums: List[int]) -> int:
        (left, right) = (0, len(nums) - 1)
        _min = float('inf')
        while left <= right:
            mid = (left + right) // 2
            left_is_sorted = nums[left] < nums[mid]
            if right - left == 1:
                return min(_min, nums[left] if nums[left] < nums[right] else nums[right])
            if left_is_sorted:
                _min = min(_min, nums[left])
                left = mid + 1
            else:
                _min = min(_min, nums[mid])
                right = mid - 1
        return _min
```

---------------------

# 2025-10-11 06:20: 278. First Bad Version (Easy) (time: 7m 33):

```python3
class Solution:

    def firstBadVersion(self, n: int) -> int:

        def isBadVersion(version: int) -> bool:
            return version >= bad
        (left, right) = (0, n)
        while left <= right:
            mid = (left + right) // 2
            is_bad = isBadVersion(mid)
            if is_bad and (not isBadVersion(mid - 1)):
                return mid
            if is_bad:
                right = mid - 1
            else:
                left = mid + 1
```

---------------------

# 2025-10-11 06:54: 34. Find First and Last Position of Element in Sorted Array (Medium) (time: 7m 47):

```python3
class Solution:

    def searchRange(self, nums: List[int], target: int) -> List[int]:

        def start():
            left = bisect_left(nums, target)
            if 0 <= left < len(nums):
                if nums[left] == target:
                    return left
            return -1

        def end():
            right = bisect_right(nums, target) - 1
            if 0 <= right < len(nums):
                if nums[right] == target:
                    return right
            return -1
        return [start(), end()]
```

---------------------

# 2025-10-11 07:53: 441. Arranging Coins (Easy) (time: 29m 50):

```python3
from math import sqrt

class Solution:

    def arrangeCoins(self, n: int) -> int:
        return int((-1 + sqrt(1 + 8 * n)) // 2)
```

## notes: 

Hm so if we think of the number of stars for a given row, it's actually n.

So if n == 10, then the number of stars in that row is 10. The total
number of stars for t rows is `t * (t + 1) / 2`. We can use the quadratic formula
to see that therefor, given the number of stars (with the last row
complete) we can compute the row with: `int((-1 + sqrt(1 + 8 * n)) // 2)`.

I did get some help from Grok for computing `int((-1 + sqrt(1 + 8 * n)) // 2)`
so need to refresh some math, ideally involving the quadratic formula.

---------------------

# 2025-10-11 08:41: 162. Find Peak Element (Medium) - learning (time: 33m 55):

```python3
class Solution:

    def findPeakElement(self, nums: list[int]) -> int:
        (left, right) = (0, len(nums) - 1)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < nums[mid + 1]:
                left = mid + 1
            else:
                right = mid
        return left
```

## notes: 

I don't know why this problem brain fries me. So i had to look up the
solution. Will need to reschedule.

---------------------

# 2025-10-11 10:01: 1011. Capacity To Ship Packages Within D Days (Medium) - learning (time: 17m 41):

```python3
class Solution:

    def daysToShipPackages(self, nums, weightPerShipment):
        total = 0
        count = 0
        for n in nums:
            if n > weightPerShipment:
                return float('inf')
            if total + n >= weightPerShipment:
                count += 1
                total = n
            else:
                total += n
        return count

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        (min_weight, max_weight) = (max(weights), sum(weights))
        while min_weight <= max_weight:
            guessWeight = (min_weight + max_weight) // 2
            daysToShip = self.daysToShipPackages(weights, guessWeight)
            if daysToShip >= days:
                min_weight = guessWeight + 1
            else:
                max_weight = guessWeight - 1
        return min_weight - 1
```

## notes: 

self.daysToShipPackages(weights, 15) is the function we can use to compute how many days
it'll take to ship packages for this given weight.

So we can perform a binary search by starting with a high number. The starting number
can by the sum of the array, which would essentially mean we can ship all the packages
in a single day.

This is essentially the number we are trying to minimize.

So self.daysToShipPackages(weights, sum(weights)) returns 1

Our minimum value for weightPerShipment should be the max size of a package in weights,
since else a package wouldn't fit any shipment.

Ugh ok this is frustrating. I know i'm very close, but somehow some tests don't pass.
I typically get confused in these minimization binary search problems
that involve increasing or decreasing values, knowing when to stop
what to return etc.

Must revisit.

---------------------

# 2025-10-11 12:40: 81. Search in Rotated Sorted Array II (Medium) (time: 17m 4):

```python3
class Solution:

    def search(self, nums: List[int], target: int) -> bool:
        n = len(nums) - 1
        (left, right) = (0, n)
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            left_is_sorted = nums[left] <= nums[mid]
            right_is_sorted = not left_is_sorted
            if nums[mid] == target:
                return True
            elif left_is_sorted:
                if nums[left] == nums[mid]:
                    left += 1
                elif nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            elif right_is_sorted:
                if nums[mid] == nums[right]:
                    right -= 1
                elif nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return False
```

---------------------

# 2025-10-11 12:50: 744. Find Smallest Letter Greater Than Target (Easy) (time: 4m 38):

```python3
class Solution:

    def findSmallestLetterGreaterThanTarget(self, letters: List[str], target: str) -> str:
        low = 0
        high = len(letters) - 1
        result = letters[0]
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if letters[mid] > target:
                result = letters[mid]
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

---------------------

# 2025-10-11 13:04: 69. Sqrt(x) (Easy) (time: 11m 55):

```python3
class Solution:

    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0
        low = 1
        high = x
        while low <= high:
            mid = low + (high - low) / 2
            res = int(mid * mid)
            if int(res) == x:
                return floor(mid)
            elif res < x:
                low = mid
            else:
                high = mid
```

---------------------

# 2025-10-12 06:03: 852. Peak Index in a Mountain Array (Medium) (time: 5m 28):

```python3
class Solution:

    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        (left, right) = (1, len(arr) - 2)
        while left <= right:
            mid = (left + right) // 2
            if arr[mid - 1] < arr[mid] > arr[mid + 1]:
                return mid
            elif arr[mid - 1] > arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
```

---------------------

# 2025-10-12 06:12: 367. Valid Perfect Square (Easy) (time: 6m 16):

```python3
class Solution:

    def isPerfectSquare(self, num: int) -> bool:
        low = 1
        high = num
        while low <= high:
            mid = low + (high - low) // 2
            guess = mid * mid
            if guess == num:
                return True
            elif guess < num:
                low = mid + 1
            else:
                high = mid - 1
        return False
```

---------------------

# 2025-10-12 07:08: 1539. Kth Missing Positive Number (Easy) - learning (time: 15m 24):

```python3
class Solution:

    def findKthPositive(self, arr: List[int], k: int) -> int:
        (left, right) = (0, len(arr) - 1)
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k
```

## notes: 

Ok so solving this problem in less than O(n) is possible
but non trivial.

The first element of the array alreasy tells us how many values
are missing from the front of the array.

So we can deduct that from k.

Then we can compute the number of missing elements between two pointers
by comparing the delta of their values with the delta of their indices.

e.g if L is at val 2, and M is at val 4, but their indices are 0 and 2,
there are no missing values. In which case is k = 2, we can go right, because
the missing value has to be on the right side.

Interesting problem, but it feels quite hard right now. Will revisit later.

---------------------

# 2025-10-12 10:18: 3701. Compute Alternating Sum (Easy) (time: 8m 38):

```python3
class Solution:

    def alternatingSum(self, nums: List[int]) -> int:
        return reduce(lambda acc, val: [sub, add][bool(val[0] % 2 == 0)](acc, val[1]), enumerate(nums), 0)
```

---------------------

# 2025-10-12 10:51: 3248. Snake in Matrix (Easy) (time: 15m 31):

```python3
class Solution:

    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        deltas = dict(RIGHT=(0, 1), LEFT=(0, -1), UP=(-1, 0), DOWN=(1, 0))
        pos = reduce(lambda acc, val: (acc[0] + deltas[val][0], acc[1] + deltas[val][1]), commands, (0, 0))
        return pos[0] * n + pos[1]
```

---------------------

# 2025-10-12 11:24: 2570. Merge Two 2D Arrays by Summing Values (Easy) (time: 12m 3):

```python3
class Solution:

    def mergeArrays(self, nums1: List[List[int]], nums2: List[List[int]]) -> List[List[int]]:
        dd = defaultdict(int)
        for (i, n) in chain(nums1, nums2):
            dd[i] += n
        return [*sorted([list(x) for x in dd.items()], key=lambda x: x[0])]
```

---------------------

# 2025-10-12 12:04: 3304. Find the K-th Character in String Game I (Easy) (time: 17m 52):

```python3
class Solution:

    def kthCharacter(self, k: int) -> str:
        L = ascii_letters
        pos = {v: i for (i, v) in enumerate(L)}
        S = 'a'
        for _ in range(10):
            T = ''.join((L[(pos[x] + 1) % 26] for x in S))
            S += T
        return S[k - 1]
```

---------------------

# 2025-10-13 08:18: Review Notes

# Review notes

## Binary Search

### Overall

Grok recently proposed i use this template:

```python
def binary_search_optimization(min_possible, max_possible, is_minimization=True):
    low = min_possible  # Smallest possible answer
    high = max_possible  # Largest possible answer
    result = -1  # Or some sentinel value; we'll update this

    while low <= high:
        mid = low + (high - low) // 2  # Avoid overflow, though Python ints are fine

        if check_condition(mid):  # Your helper function: True if mid satisfies the goal
            result = mid  # This is a candidate answer
            if is_minimization:
                high = mid - 1  # Try to find a smaller valid mid
            else:
                low = mid + 1   # Try to find a larger valid mid
        else:
            if is_minimization:
                low = mid + 1   # Need a larger mid to satisfy condition
            else:
                high = mid - 1  # Need a smaller mid to satisfy condition

    return result  # After loop, result holds the optimal value
```

I've started using it for optimization binary search problems, and can confirm in many cases it's as easy to pasting it in (i have a snippet), writing the check condition and it just works.

I'd love to have more opportunities to use this template on a variety of binary search optimization problems.

### 704. Binary Search

Straight up no frills binary search question.

```
mid = (left + right) // 2
```

I realise this is suboptimal but i can get away with it in Python.

### 153. Find Minimum in Rotated Sorted Array

I'm glad i was able to crack this. I'm sure there's a simpler and more elegant solution than the one i wrote, but nevertheless, it seems optimial.

The key was noticing that the left and right pointer can be used to determine on which side min is, so decide whether to go left or right.

### 278. First Bad Version

Pretty easy question really. Wonder if i can minimize the number of calls to isBadVersion as it seems i'm calling it twice. But anyhow happy with this solve.

### 34. Find First and Last Position of Element in Sorted Array

Leveraging `bisect_left` and `bisect_right` for binary search is a pattern i want to use more. Bisecting and binary aren't the exact same thing, and i'm considering creating a snippet to use bisecting to find an element as it's the kind of thing that can shave off a few seconds or minute during a solve.

### 3512. Minimum Operations to Make Array Sum Divisible by K

I'm happy with this solve, as my solution is as simple as it gets, and it correctly leverages the fact one can check divisibility on the entire array modulo k, without being concerned with individual elements.

### 33. Search in Rotated Sorted Array

I've always struggled with this question in the past, but the pattern is getting reinforced of late, so i think i should be good with it going forwards.

## Linked Lists

### 206. Reverse Linked List

This is also something i've struggled with. But i'm starting to build the muscle memory for this pattern:

```python3
def reverseList(self, h: Optional[ListNode]) -> Optional[ListNode]:
    d = ListNode(0)
    while h:
        d.next, h.next, h = h, d.next, h.next
    return d.next
```

The dummy node is crucial. For the inside of the while loop, i have a mnemonic to remember `d.next, h.next, h`, then i copy and paste it to the right side of the equal sign, and move the `h` to the first position.

I'm not proud of having to use these little mnemonic hacks, but they do the job. Being able to internally visualize what these pointers are doing is kind of hard without a lot of practice.

### 21. Merge Two Sorted Lists

I'm not super proud of my approach because i'm certain there are much simpler ones (it's quite verbose), but it works. This is a mental model i use a lot it seems: you can just pop elements off the front of a linked list. It's more code, but popping and merging is a very easy mental model to work with. Just write your popping functions correctly, and it just works.

### 141. Linked List Cycle

This is a problem i'm quite comfortable with now. Though i'm sure my solution can be simplified, especially the conditional statement.

### 234. Palindrome Linked List

This solution feels like a hack, because i'm first converting the linked list into a double linked list. It feels like a hack, but apparently this solution is acceptable.

### 876. Middle of the Linked List

I struggled with this question in the past but i'm happy with this solve. The fast pointer makes it optimal.

---

I've mentally rehearsed linked list reversal, and cycle detection as suggested.

## Quick Quiz: explain two problems.

### 238. Product of Array Except Self

What really helps solving this question is using letters for variables rather than numbers. For example a list with a, b, c, d.

let's accumulate the product from left to right:

```
a, ab, abc, abcd
```

and from right to left:

```
abcd, bcd, cd, d
```

Now let's take the product of these two product arrays:

```
a^2bcd, ab^2cd, abc^2d, abcd^2
```

This is not what we're after. But we notice that since the array elements are squared,
we could add 1 at the start of the lists, and drop the last element to get:

```
1, a, ab, abc
dcb, dc, d, 1
```

Then take their products to get:

```
bcd, adc, abd, abc
```

which is the product of the array except self.

Another approach is to take the product of the array:

```
abcd, abcd, abcd, abcd
```

And divide each product with self:

```
abcd/a, abcd/b, abcd/c, abcd/d
```

This is, however, more complex since we have to cater for negative values. This solution is possible to compute, just more complex. My fav solution to this question is:

```python
def productExceptSelf(nums):
    ans = [1] * len(nums)
    left, right = 1, 1
    for i in range(len(nums)):
        ans[i] *= left
        ans[~i] *= right
        left *= nums[i]
        right *= nums[~i]
    return ans
```

I still struggle being able to implement it when solving. It's extremely creative and elegant (credit: Stephan Pochmann). We start with `ans = [1,1,1,1]`. In the iteration, we times equals `ans[i]` and `ans[~i]` with the left and right variables. The use of `~i` the complement of i to access the list in reverse, in python, is nothing short of genius.

We then times equal `left` and `right` with `nums[i]` and `nums[~i]` respectively. Since we do so _after_ using them to times equals the `ans` list, this cates for the offset of each direction by 1. Simply genius.

### 543. Diameter of Binary Tree

This question seems easy at first, but is actually medium (or medium hard) at the very least. The reason being that it's not simply the distance from the left-most to the right-most, via the root. It's the max distance from any node to any node, which may or may not pass by the root.

Working your way to the solution is hard, yet the solution itself is extremely simple. The solution is a recursive DFS. We return the `max` of `left` and `right` `+1`. `left` and `right` are the result of the `dfs` call on the left and right children. The `+1` ensure that we increment the depth of each recursion, which take care of tracking the maximum depth of the binary tree on the left and right side.

Then, the maximum diameter is tracked in a mutable variable (e.g on self.diam). We take the `max` of `self.diam` and `left + right`.

In retrospect, it's easy. During the solve, it isn't.

---------------------

# 2025-10-13 10:54: 703. Kth Largest Element in a Stream (Easy) (time: 1m 17):

```python3
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.nums = nums
        self.k = k

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort()
        return self.nums[-self.k]
```

## notes: 

The solution obviously requires a heap, but i wasted time getting started on it,
for some reason, so will try submitting this brute force method for now,
and revisit this question later with a proper heap implementation.

---------------------

# 2025-10-13 11:01: 347. Top K Frequent Elements (Medium) (time: 2m 39):

```python3
class Solution:

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        c = list(dict(Counter(nums)).items())
        c.sort(key=lambda x: -x[1])
        return [x[0] for x in c[:k]]
```

## notes: 

This is an easy solve with a Counter, but clearly suboptimal.

---------------------

# 2025-10-13 11:42: 133. Clone Graph (Medium) (time: 16m 23):

```python3
import copy

class Solution:

    def cloneGraph(self, node: Optional[GraphNode]) -> Optional[GraphNode]:
        return copy.deepcopy(node)
```

## notes: 

Ok the top comment in the discussion is: "Am I the only one who can't understand the question even after going through it several times??"

So clearly many people are finding this question hard to understand.. myself included.

Next comment:

??????????????
What does this question mean???

Next comment:

****** Question.

So i just cheated by using copy.deepcopy, because the question seemed poorly worded. Here's a good solution from the solutions section of leetcode:

def cloneGraph(self, node: 'Node') -> 'Node':
        old_to_new = {}

        def clone(node):
            if node in old_to_new:
                return old_to_new[node]

            copy = Node(node.val)
            old_to_new[node] = copy

            for nei in node.neighbors:
                copy.neighbors.append(clone(nei))
            return copy

        return clone(node) if node else None

---------------------

# 2025-10-13 12:58: 3340. Check Balanced String (Easy) (time: 3m 52):

```python3
class Solution:

    def isBalanced(self, num: str) -> bool:
        (sum_odd, sum_even) = (0, 0)
        for (i, n) in enumerate(num):
            if i % 2 == 0:
                sum_even += int(n)
            else:
                sum_odd += int(n)
        return sum_odd == sum_even
```

---------------------

# 2025-10-13 15:44: 1046. Last Stone Weight (Easy) (time: 6m 10):

```python3
class Solution:

    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-x for x in stones]
        heapify(stones)
        while True:
            if len(stones) == 1:
                return -stones[0]
            elif len(stones) == 0:
                return 0
            y = -heappop(stones)
            x = -heappop(stones)
            if x == y:
                continue
            heappush(stones, -(y - x))
```

---------------------

# 2025-10-13 15:54: 2500. Delete Greatest Value in Each Row (Easy) (time: 7m 31):

```python3
class Solution:

    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        for row in grid:
            heapify(row)
        return sum((max((heappop(row) for row in grid)) for _ in range(len(grid[0]))))
```

---------------------

# 2025-10-13 16:04: 451. Sort Characters By Frequency (Medium) (time: 3m 22):

```python3
class Solution:

    def frequencySort(self, s: str) -> str:
        c = list(dict(Counter(s)).items())
        c.sort(key=lambda x: x[1], reverse=True)
        return ''.join([x[0] * x[1] for x in c])
```

---------------------

# 2025-10-13 16:17: 1337. The K Weakest Rows in a Matrix (Easy) (time: 5m 49):

```python3
class Solution:

    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        mat = [*sorted(enumerate(mat), key=lambda x: (sum((e == 1 for e in x[1])), x[0]))]
        return [x[0] for x in mat][:k]
```

---------------------

# 2025-10-13 16:57: 1792. Maximize Score After N Operations (Medium) - learning (time: 34m 16):

```python3
from typing import List
from math import gcd
from itertools import islice

class Solution:

    def maxScore(self, nums: List[int]) -> int:
        combs = [*combinations(nums, 2)]
        combs.sort(key=lambda x: gcd(*x), reverse=True)
        groups = islice(sorted([gcd(*x) for x in combs], reverse=True), 0, len(nums) // 2)
        groups = [*groups][::-1]
        return sum((x[0] * x[1] for x in enumerate(groups, start=1)))
```

## notes: 

Hm the not so simple here is deciding which elements to pick from the array to maximize
the result.

Let's run through some options by hand, and see whether we can spot a pattern.

[3,4,6,8]

Here are all the options we have for GCD

gcd(3, 4) -> 1
gcd(3, 6) -> 3
gcd(3, 8) -> 1
gcd(4, 6) -> 2
gcd(4, 8) -> 4
gcd(6, 8) -> 2

The best picks are, and we note they have the greatest GCDs:

gcd(3, 6) -> 3
gcd(4, 8) -> 4

I'm not really sure what the whole 'n' business is about, since we don't get passed an n. Maybe they
mean that n = len(nums) // 2.

Looking at the provided hints:

Hint 1
Find every way to split the array until n groups of 2. Brute force recursion is acceptable.
Hint 2
Calculate the gcd of every pair and greedily multiply the largest gcds.

I'm not really clear what hint 1 means. If we want groups of 2, we don't get to choose how many groups we get.

For example: `[*combinations(nums, 2)]` gives us:

[(3, 4), (3, 6), (3, 8), (4, 6), (4, 8), (6, 8)]

We can take their gcds:

[1, 3, 1, 2, 4, 2]

sort it and take the two largest numbers.

groups = islice(
    sorted([gcd(*x) for x in combinations(nums, 2)], reverse=True),
    0,
    len(nums) // 2,
)
groups = [*groups][::-1]
return sum(x[0] * x[1] for x in enumerate(groups, start=1))

This works for the given example. But it might be by chance. Let's try others.

Works on many values, but not on:

# assert sol.maxScore([1, 2, 3, 6]) == 7
# assert sol.maxScore([9, 3, 6, 2]) == 8
# assert sol.maxScore([1, 2, 3, 4, 5, 6]) == 14

ok i can see what the problem is. The problem is, combinations leads to repeats, which breaks the constraints.
So i'd need to write a recursive function which breaks up the array into groups of two, without repeats.

I'm a bit rusty with this.. very similar to knapsack in a way. Will revisit this soon.

---------------------

# 2025-10-13 20:13: 506. Relative Ranks (Easy) (time: 6m 9):

```python3
class Solution:

    def findRelativeRanks(self, score: List[int]) -> List[str]:
        r = {1: 'Gold Medal', 2: 'Silver Medal', 3: 'Bronze Medal'}
        orig = score[:]
        score.sort(reverse=True)
        ranks = {}
        for (i, v) in enumerate(score, start=1):
            ranks[v] = r.get(i, f'{i}')
        return [ranks[x] for x in orig]
```

---------------------

# 2025-10-13 20:29: 2357. Make Array Zero by Subtracting Equal Amounts (Easy) (time: 8m 12):

```python3
class Solution:

    def minimumOperations(self, nums: List[int]) -> int:
        return len(set([x for x in nums if x != 0]))
```

---------------------

# 2025-10-13 20:51: 378. Kth Smallest Element in a Sorted Matrix (Medium) (time: 11m 58):

```python3
class Solution:

    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        heap = []
        for (i, row) in enumerate(matrix):
            heappush(heap, (row[0], i, 0))
        for i in range(k - 1):
            (val, row, col) = heappop(heap)
            if col + 1 < len(matrix):
                heappush(heap, (matrix[row][col + 1], row, col + 1))
        return heap[0][0]
```

## notes: 

I came up with a solution involving sort, so didn't follow the explicit memory constraints.

Had to look up a solution. k-way merge. Great solution. Will have to revisit.

---------------------

# 2025-10-14 06:38: 2231. Largest Number After Digit Swaps by Parity (Easy) (time: 25m 56):

```python3
class Solution:

    def largestInteger(self, num: int) -> int:
        nums = [int(x) for x in str(num)]
        parity = [x % 2 != 0 for x in nums]
        odd = [*compress(nums, [x % 2 != 0 for x in nums])]
        even = [*compress(nums, [x % 2 == 0 for x in nums])]
        odd.sort(reverse=True)
        even.sort(reverse=True)
        res = []
        for p in parity:
            if p:
                res.append(odd.pop(0))
            else:
                res.append(even.pop(0))
        return int(''.join((str(x) for x in res)))
```

## notes: 

Had to look at the hints. Also i'm sure there's a cleaner way of doing this using
a heap.

---------------------

# 2025-10-14 06:55: 692. Top K Frequent Words (Medium) (time: 8m 40):

```python3
class Solution:

    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        counts = [(-count, word) for (word, count) in Counter(words).items()]
        heapify(counts)
        return [heappop(counts)[1] for _ in range(k)]
```

---------------------

# 2025-10-14 07:55: 215. Kth Largest Element in an Array (Medium) (time: 17m 26):

```python3
from rich import print

class Solution:

    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        verbose = False
        for n in nums:
            if len(heap) < k:
                heappush(heap, n)
                continue
            elif n > heap[0]:
                pop = heappop(heap)
                heappush(heap, n)
        return heap[0]
```

## notes: 

I was able to solve this quickly. I still find it unintiuitive for some reason
that i can use a minheap to track the k largest elements.

[1]


[1]
 /
[2]
n: 3 is larger than the top of the heap (1) so popping 1, and pushing 3


[2]
 /
[3]
n: 4 is larger than the top of the heap (2) so popping 2, and pushing 4


[3]
 /
[4]
n: 5 is larger than the top of the heap (3) so popping 3, and pushing 5


[4]
 /
[5]
n: 6 is larger than the top of the heap (4) so popping 4, and pushing 6


[5]
 /
[6]
5

Printing out what's happening does help a bit. The min propery of the heap is useful
because we can efficiently pop the min element. We're efficiently clearing the smallest
elements, so all that's left are the largest elements.

---------------------

# 2025-10-14 10:37: 767. Reorganize String (Medium) - learning (time: 22m 14):

```python3
class Solution:

    def reorganizeString(self, S):
        (res, c) = ([], Counter(S))
        pq = [(-value, key) for (key, value) in c.items()]
        heapify(pq)
        (prev_count, prev_char) = (0, '')
        while pq:
            (count, char) = heappop(pq)
            res += [char]
            if prev_count < 0:
                heappush(pq, (prev_count, prev_char))
            count += 1
            (prev_count, prev_char) = (count, char)
        res = ''.join(res)
        if len(res) != len(S):
            return ''
        return res
```

## notes: 

Failed. Had to look up the solution.

So great solution. We put the counts on a heap, which i'd imagined could be the case,
then we alternate between using the top element, and the prev element.

I'd come close to this solution, but not quite. I didn't think of using a prev
to alternate.

---------------------

# 2025-10-14 11:32: 973. K Closest Points to Origin (Medium):

```python3
class Solution:

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for (x, y) in points:
            d = -sqrt(x * x + y * y)
            if len(heap) < k:
                heappush(heap, (d, [x, y]))
            elif d > heap[0][0]:
                heappop(heap)
                heappush(heap, (d, [x, y]))
        return [x[1] for x in nlargest(k, heap)]
```

---------------------

# 2025-10-14 12:17: 621. Task Scheduler (Medium) - learning (time: 43m 21):

```python3
class Solution:

    def leastInterval(self, tasks: List[str], n: int) -> int:
        if not tasks:
            return 0
        freq = Counter(tasks)
        max_heap = [-count for count in freq.values()]
        heapify(max_heap)
        time = 0
        cooldown = deque()
        while max_heap or cooldown:
            time += 1
            while cooldown and cooldown[0][0] <= time:
                heappush(max_heap, cooldown.popleft()[1])
            if max_heap:
                remaining = heappop(max_heap) + 1
                if remaining:
                    cooldown.append((time + n + 1, remaining))
        return time
```

## notes: 

Alright so i guess we need to put the counts on a min heap, containing the (cooloff, count, char).
The cooloff is when we'll be able to use the task next (i.e current time + n).
So we pop the min from the heap, use it, decrement it, and increment its cooloff.
Then the next task available will have the smallest cooloff period.
If no task is available, we add a count of one to the time taken.

Hmm i got close. But not all tests are passing. So i'll look at the solution.

---------------------

# 2025-10-14 14:56: 2119. A Number After a Double Reversal (Easy) (time: 3m 50):

```python3
class Solution:

    def isSameAfterReversals(self, num: int) -> bool:

        def rev(n):
            r = 0
            while n:
                r *= 10
                r += n % 10
                n //= 10
            return r
        reversed1 = rev(num)
        reversed2 = rev(reversed1)
        return reversed2 == num
```

---------------------

# 2025-10-14 15:12: 561. Array Partition (Easy) (time: 7m 32):

```python3
class Solution:

    def arrayPairSum(self, nums: List[int]) -> int:

        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for (a, b) in zip_longest(r, r[1:])]
        return sum((min(a, b) for (a, b) in batched(sorted(nums), 2)))
```

---------------------

# 2025-10-14 15:28: 2103. Rings and Rods (Easy) (time: 6m 48):

```python3
class Solution:

    def countPoints(self, rings: str) -> int:

        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for (a, b) in zip_longest(r, r[1:])]
        rods = defaultdict(set)
        for (col, rod) in batched(rings, 2):
            rods[int(rod)].add(col)
        full = set('RGB')
        return sum((x == full for x in rods.values()))
```

---------------------

# 2025-10-14 15:48: 2129. Capitalize the Title (Easy) (time: 1m 13):

```python3
class Solution:

    def capitalizeTitle(self, title: str) -> str:
        return ' '.join((w.lower() if len(w) <= 2 else w[0].upper() + w[1:].lower() for w in title.split()))
```

---------------------

# 2025-10-14 17:47: 3019. Number of Changing Keys (Easy) (time: 3m 46):

```python3
class Solution:

    def countKeyChanges(self, s: str) -> int:
        return sum((a != b for (a, b) in pairwise(s.lower())))
```

---------------------

# 2025-10-14 17:53: 2980. Check if Bitwise OR Has Trailing Zeros (Easy) (time: 3m 29):

```python3
class Solution:

    def hasTrailingZeros(self, nums: List[int]) -> bool:
        return sum((x % 2 == 0 for x in nums)) >= 2
```

---------------------

# 2025-10-14 18:01: 78. Subsets (Medium) (time: 3m 59):

```python3
class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:
        return [*chain(*[[*combinations(nums, n)] for n in range(len(nums) + 1)])]
```

---------------------

# 2025-10-14 18:49: 2527. Find Xor-Beauty of Array (Medium) - learning (time: 38m 42):

```python3
class Solution:

    def xorBeautyBruteForce(self, nums: List[int]) -> int:
        effective = lambda i, j, k: (nums[i] | nums[j]) & nums[k]
        return reduce(ixor, starmap(effective, product(range(len(nums)), range(len(nums)), range(len(nums)))))

    def xorBeautyBruteForce2(self, nums: List[int]) -> int:
        effective = lambda i, k: nums[i] & nums[k]
        return reduce(ixor, starmap(effective, product(range(len(nums)), range(len(nums)))))

    def xorBeauty(self, nums: List[int]) -> int:
        return reduce(ixor, nums)
```

## notes: 

Ok so i could brute force this one, but then TLE. I tried following the hints,
but was stumped.

Looking at solutions.. someone in discussion said "just xor the array" which indeed works.

Will need to revisit:

https://leetcode.com/problems/find-xor-beauty-of-array/solutions/3014972/python3-one-liner-with-formal-proof/

I totally understand the proof. But making the leap triplet combinations to discarding unnecessary computations
still feels like a big leap.

---------------------

# 2025-10-15 06:38: 1356. Sort Integers by The Number of 1 Bits (Easy) (time: 7m 8):

```python3
class Solution:

    def sortByBits(self, arr: List[int]) -> List[int]:

        def count_ones(num):
            res = 0
            while num:
                res += 1
                num &= num - 1
            return res
        return [*sorted(arr, key=lambda x: (count_ones(x), x))]
```

---------------------

# 2025-10-15 06:56: 2044. Count Number of Maximum Bitwise-OR Subsets (Medium) (time: 7m 4):

```python3
class Solution:

    def countMaxOrSubsets(self, nums: List[int]) -> int:
        _max = reduce(or_, nums)
        return sum((reduce(or_, s) == _max for s in chain(*[[*combinations(nums, i)] for i in range(1, len(nums) + 1)])))
```

---------------------

# 2025-10-15 08:26: 2433. Find The Original Array of Prefix Xor (Medium) - learning (time: 29m 15):

```python3
class Solution:

    def findArray(self, pref: List[int]) -> List[int]:
        prev = pref[0]
        for i in range(1, len(pref)):
            pref[i] ^= prev
            prev ^= pref[i]
        return pref
```

## notes: 

I don't know why this problem is completely frying my brain. I'm so bad at DP it's ridiculous, i look at the xors, and numbers
and my brain freezes. I know this is a super simple DP problem, and yet my brain freezes.

https://leetcode.com/problems/find-the-original-array-of-prefix-xor/solutions/4228796/video-give-me-5-minutes-how-we-think-about-a-solution-python-javascript-java-c/

Revisit.

---------------------

# 2025-10-15 09:12: 1310. XOR Queries of a Subarray (Medium) (time: 11m 19):

```python3
class Solution:

    def get_xor_range(self, i, j, arr):
        return reduce(xor, arr[i:j + 1])

    def xorQueriesBruteForce(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        return [self.get_xor_range(i, j, arr) for (i, j) in queries]

    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        prefix = [*accumulate(arr, func=xor)] + [0]

        def get_range(i, j):
            return prefix[j] ^ prefix[i - 1]
        return [get_range(i, j) for (i, j) in queries]
```

## notes: 

This seems like a prefix computation of the xors.. so rather than recomputing
the xors within a range each time, they can be precomputed.

I'll do it the brute force way first, so i can compare.

Alright so brute force was easy. Now if we think of the prefix approach,
with simple data: 1, 2, 3

In binary that's

1, 10, 101

let's compute the range: 1, [10, 101]

2 ^ 3 is 1, so we're effectively trying to compute 1, [1]

Now if we accumulate the xors, we get:

1, 11, 0

Which i'm guessing is:

prefix[j] ^ prefix[i-1]

---------------------

# 2025-10-15 10:13: 240. Search a 2D Matrix II (Medium) (time: 61m 15):

```python3
class Solution:

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        max_row = bisect_right([x[0] for x in matrix], target)
        if max_row < 0:
            max_row = 0
        if max_row >= len(matrix):
            max_row = len(matrix) - 1
        max_col = bisect_right(matrix[0], target)
        if max_col < 0:
            max_col = 0
        if max_col >= len(matrix[0]):
            max_col = len(matrix[0]) - 1
        for r in range(max_row + 1):
            ind = bisect_left(matrix[r][:max_col], target)
            if 0 <= ind < len(matrix[r]):
                if matrix[r][ind] == target:
                    return True
        return False
```

## notes: 

Ok this seems pretty straight forward: serach for which row the entry
might be in, this can be done by doing a bisect of the first
column.

So the first column is: [1, 2, 3, 10, 18]
at indices:              0, 1, 2, 3, 4


>>> bisect_left([1, 2, 3, 10, 18], 0)
0

>>> bisect_right([1, 2, 3, 10, 18], 0)
0

>>> bisect_left([1, 2, 3, 10, 18], 5)
3

>>> bisect_right([1, 2, 3, 10, 18], 5)
3

>>> bisect_left([1, 2, 3, 10, 18], 30)
5

>>> bisect_right([1, 2, 3, 10, 18], 30)
5

I'm trying to decide whether to use bisect left, or right. Might be better to get bisect_left - 1


>>> bisect_left([1, 2, 3, 10, 18], 0) - 1
-1

It's useful to know we're out of bounds.

>>> bisect_left([1, 2, 3, 10, 18], 5) -1
2

Hmm no wait, this won't work because even though we get row 2, target is actually in row 1.
So bisecting the first column won't work.

We need to use the dual constraint of rows and column being sorted.

So if the number is greater than row[0] and smaller than row[-1], we can search that row.
In the case of 5, that gives us rows: 0, 1, 2.

Then we can use the column constraint to find the column. Using bisect again, if we do a
bisect right of the first row, we should get the column.

>>> bisect_left([1, 4, 7, 11, 15], 5) -1
1

This potentially gives us a column, but again, not really, because 5 could be some place else
while maintaining that constraint. So bisect isn't going to work.

Ok so with binary search, we can exclude rows and columns from the search. If target is smaller
than the first item in a row, then we can discard the rows that are greater from the search.

So i think we can only achieve range reduction.. then we'll have to search a bunch of rows and columns.

Ok got it in the end. Kind of painful, and the code isn't super clean. Also bisect isn't as efficient
as doing a bs by hand, because of array slicing.

Super interesting problem nevertheless.

---------------------

# 2025-10-15 12:32: 322. Coin Change (Medium) - learning (time: 131m 51):

```python3
class Solution:

    def coinChangeGreedy(self, coins: List[int], amount: int) -> int:
        coins.sort(reverse=True)
        res = []
        for c in coins:
            if c <= amount:
                (div, mod) = divmod(amount, c)
                res.extend([c] * div)
                amount = mod
        return len(res) if amount == 0 else -1

    def coinChange(self, coins, amount):
        coins = sorted(coins)
        per_dp = []
        for _ in coins:
            row = [''] * (amount + 1)
            row[0] = 0
            per_dp.append(row)
        for (i, coin) in enumerate(coins):
            for x in range(coin, amount + 1):
                num_coins = per_dp[i][x - coin]
                if num_coins != '':
                    per_dp[i][x] = num_coins + 1
        table_data = [[coins[i]] + per_dp[i] for i in range(len(coins))]
        cum_dp = [maxsize] * (amount + 1)
        cum_dp[0] = 0
        for coin in coins:
            for x in range(coin, amount + 1):
                if cum_dp[x - coin] != maxsize:
                    cum_dp[x] = min(cum_dp[x], cum_dp[x - coin] + 1)
        return cum_dp[amount] if cum_dp[amount] != maxsize else -1
```

## notes: 

Greedy method fails on some test cases, due to "non-uniformity".

Looking at discussions for hints.

Hint:

> Take coins=[1,2,5] and amount = 11 as an example,
>
>     If I use one 1, I need to know the fewest number of coins I need to make up 10, i.e., dp[10]. Overall I need 1+dp[10] coins.
>     If I use one 2, I need 1+dp[9] coins.
>     If I use one 5, I need 1+dp[6] coins.
>
> Therefore, I need to calculate dp from 1 to amount.

yeahhh that doesn't help either. I'm going to look up the solution. I'm already glad i managed
to come up with the greedy solution.

Ok the optimial DP based solution didn't make sense.. so i turned it into a 2D problem,
using tabulate to see the coins needed for each value ranging from coin to amount,
for each denomination.

  coin    0  1    2    3    4    5    6    7    8    9    10
------  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ----
     1    0  1    2    3    4    5    6    7    8    9    10
     2    0       1         2         3         4         5
     3    0            1              2              3
     4    0                 1                   2
     5    0                      1                        2
     6    0                           1
     7    0                                1
     8    0                                     1
     9    0                                          1
    10    0                                               1
--------
0 1 1 1 1 1 1 1 1 1 1

Final result: 1

then we take the cummulative min.

Honestly this makes it so much easier undertanding what's going on.

---------------------

# 2025-10-15 12:48: 3688. Bitwise OR of Even Numbers in an Array (Easy) (time: 2m 32):

```python3
class Solution:

    def evenNumberBitwiseORs(self, nums: List[int]) -> int:
        return reduce(or_, filter(lambda x: x % 2 == 0, nums), 0)
```

---------------------

# 2025-10-15 13:03: 3158. Find the XOR of Numbers Which Appear Twice (Easy) (time: 10m 24):

```python3
class Solution:

    def duplicateNumbersXOR(self, nums: List[int]) -> int:
        return reduce(xor, map(lambda x: x[0], filter(lambda x: x[1] == 2, Counter(nums).items())), 0)
```

## notes: 

This is a bit manipulation problem, so let's think whether we can use
a property of xor to solve it.

We know that taking the xor of the same number yields 0

[1,2,1,3]

So if we take the xor of the entire array, we'll end up with the bitwise xor
of 2 and 3, which is `1`, and the bitwise or of the entire array is `3`.

Nope. Can't think of a clever trick we can use. So i'll use a Counter instead.

---------------------

# 2025-10-15 17:00: 300. Longest Increasing Subsequence (Medium) (time: 18m 26):

```python3
class Solution:

    def lengthOfLIS(self, nums: List[int]) -> int:
        DP = [1] * len(nums)
        for i in range(1, len(nums)):
            max_increasing = 0
            for j in range(i):
                if nums[j] < nums[i]:
                    max_increasing = max(max_increasing, DP[j])
            DP[i] = max_increasing + 1
        return max(DP)
```

## notes: 

Someone dropped some hints in the discussion, so was able to solve it. However,
this is an O(n^2) solution, not O(n log(n)).
I could revisit this later to try a more optimal solution.

---------------------

# 2025-10-15 17:39: 1011. Capacity To Ship Packages Within D Days (Medium) (time: 20m 9):

```python3
class Solution:

    def daysToShipPackages(self, nums, weightPerShipment):
        days = 1
        total = 0
        for n in nums:
            if total + n > weightPerShipment:
                days += 1
                total = n
            else:
                total += n
        return days

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        low = max(weights)
        high = sum(weights)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if self.daysToShipPackages(weights, mid) <= days:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

This went a lot smoother this time, thanks for the binary search template.

---------------------

# 2025-10-16 06:36: 2032. Two Out of Three (Easy) (time: 14m 41):

```python3
class Solution:

    def twoOutOfThree(self, nums1: List[int], nums2: List[int], nums3: List[int]) -> List[int]:
        a = set(nums1)
        b = set(nums2)
        c = set(nums3)
        res = set([])
        for v in a | b | c:
            if v in a and v in b or (v in b and v in c) or (v in a and v in c):
                res.add(v)
        return list(res)
```

---------------------

# 2025-10-16 06:44: 3370. Smallest Number With All Set Bits (Easy) (time: 5m 32):

```python3
class Solution:

    def smallestNumber(self, n: int) -> int:
        r = 1
        while True:
            if r >= n:
                return r
            r = r << 1 | 1
```

---------------------

# 2025-10-16 06:55: 2932. Maximum Strong Pair XOR I (Easy) (time: 8m 34):

```python3
class Solution:

    def maximumStrongPairXor(self, nums: List[int]) -> int:
        return max((x ^ y for (x, y) in ((x, y) for (x, y) in product(nums, nums) if abs(x - y) <= min(x, y))))
```

---------------------

# 2025-10-16 07:06: 2351. First Letter to Appear Twice (Easy) (time: 8m 39):

```python3
class Solution:

    def repeatedCharacter(self, s: str) -> str:
        seen = set([])
        for v in s:
            if v not in seen:
                seen.add(v)
            else:
                return v
```

---------------------

# 2025-10-16 07:50: 3314. Construct the Minimum Bitwise Array I (Easy) (time: 17m 29):

```python3
class Solution:

    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        res = [-1] * len(nums)
        for i in range(len(nums)):
            for j in range(nums[i]):
                if j | j + 1 == nums[i]:
                    res[i] = j
                    break
        return res
```

## notes: 

What where're really looking for is x | (x + 1) = y, and also minimize x.

nusm.       ans.
101     =>  100     |   (100 + 1)
111     =>  11      |   (11 + 1)
1011    =>  1001    |   (1001 + 1)
1101    =>  1110    |   (1110 + 1)

Thought there'd be a smart solution, but no the hint is just to bruteforce.

---------------------

# 2025-10-16 08:13: 875. Koko Eating Bananas (Medium) (time: 7m 7):

```python3
class Solution:

    def hoursToEatPiles(self, piles, k):
        h = 0
        for p in piles:
            (div, mod) = divmod(p, k)
            h += div
            if mod:
                h += 1
        return h

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        low = 1
        high = sum(piles)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if self.hoursToEatPiles(piles, mid) <= h:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

Once again, using the minimization template made this a breeze.

---------------------

# 2025-10-16 09:39: 70. Climbing Stairs (Easy) (time: 13m 49):

```python3
class Solution:

    def climbStairs(self, n: int) -> int:
        dp = [maxsize] * n
        dp[0] = 1
        dp[1] = 2
        for i in range(2, n):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[-1]
```

## notes: 

Alright so i'm not too sure how this template applies to this problem, so
let's work through this problem step by step (pun intended).


              5
             ___
          3 |
         ---
     2  |
    ---
 1 |
---

- on step 1, there's only one way of getting there
- on step 2, there's two ways, i.e 1+1 or 2
- on step 3, there's 3 ways of getting there: 1+1+1, 2+1, 1+2
- on step 4, there's at least 5 ways i can count getting there: 1+1+1+1, 1+1+2, 1+2+1, 2+2+1+1, 2+2

Ok the pattern looks like fibbonacci. So we could compute fib using DP. I pasted in the template (lcdpbottomup):

def dp_problem(self, nums: List[int], target: int) -> int:  # Adapt params to your problem
    # Step 1: Define DP array (dp[i] = optimal for first i elements or value i)
    n = len(nums)  # Or target + 1 for amount-based (e.g., Coin Change)
    dp = [sys.maxsize] * (n + 1)  # Or [0] * (n + 1); use maxsize for min, 0 for max/count
    dp[0] = 0  # Base case: dp[0] is often 0 (empty/no cost)

    # Step 2: Fill DP table bottom-up
    for i in range(1, n + 1):  # Or range(1, target + 1) for amount-based
        # For each i, compute min/max from previous states
        for choice in nums:  # Or range(i) for subsequence (e.g., LIS)
            if i - choice >= 0:  # Valid transition? (e.g., coin <= amount)
                # Transition: dp[i] = min/max(dp[i], dp[i - choice] + 1)  # Adapt +1/-cost/etc.
                dp[i] = min(dp[i], dp[i - choice] + 1)  # Example for min coins

    # Step 3: Return result (dp[n] or dp[target]; handle impossible cases)
    return dp[n] if dp[n] != sys.maxsize else -1  # Adapt for your problem

I ended up getting rid of most of it, but i guess it provided a starting point.

---------------------

# 2025-10-16 10:21: 746. Min Cost Climbing Stairs (Easy) (time: 11m 39):

```python3
class Solution:

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        for i in range(2, len(cost)):
            cost[i] = min(cost[i - 1], cost[i - 2]) + cost[i]
        return min(cost[-1], cost[-2])
```

## notes: 

Alright let's try blindly using the template, and see if we can modify it.

Nice. Even managed to do it in place. So no extra memory required.

---------------------

# 2025-10-16 13:01: 91. Decode Ways (Medium) - learning (time: 73m 55):

```python3
class Solution:

    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n + 1):
            one_digit = int(s[i - 1:i])
            two_digits = int(s[i - 2:i])
            if one_digit != 0:
                dp[i] += dp[i - 1]
            if 10 <= two_digits <= 26:
                dp[i] += dp[i - 2]
        return dp[n]
```

## notes: 

I was going in the right direction, but i guess i'm not good enough yet with DP:


class Solution:
    def numDecodings(self, s: str) -> int:
        S = [int(x) for x in s]
        n = len(S)
        invalid = "_"
        dp = [[invalid] * (n + 1), [invalid] * (n + 1)]
        dp[0][0] = 0
        dp[1][0] = 0

        def is_valid(a, b=None):
            if b is None:
                return a > 0
            else:
                if a == 0:
                    return False
                num = a + b
                return num <= 26

        for i in range(1, n + 1):
            curr = S[i - 1]
            if is_valid(curr):
                dp[0][i] = 1

        rich_print(tabulate([dp[0]], headers=["Letter"] + [asc[int(x)] for x in s]))

        for i in range(2, n + 1, 2):
            prev = S[i - 2]
            curr = S[i - 1]
            if prev != 0 and (prev * 10) + curr <= 26:
                dp[1][i] = int(is_valid((prev * 10) + curr))

        # print("")

        rich_print(tabulate([dp[1]], headers=["Letter"] + S))

Yeah it's a mess.

Looked up the solution: https://leetcode.com/problems/decode-ways/solutions/4454037/97-43-easy-solution-with-explanation/

Will need to revisit this problem soon.

---------------------

# 2025-10-16 13:25: 2656. Maximum Sum With Exactly K Elements (Easy) (time: 4m 45):

```python3
class Solution:

    def maximizeSum(self, nums: List[int], k: int) -> int:
        m = max(nums)
        res = 0
        for _ in range(k):
            res += m
            m += 1
        return res
```

---------------------

# 2025-10-16 14:43: 1143. Longest Common Subsequence (Medium) - learning (time: 64m 58):

```python3
class Solution:

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        dp = [[0 for i in range(len(text2) + 1)] for j in range(len(text1) + 1)]
        text1 = ' ' + text1
        text2 = ' ' + text2
        for i in range(1, len(text1)):
            for j in range(1, len(text2)):
                if text1[i] == text2[j]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[-1][-1]
```

## notes: 

Failed so looking up a solution.

This solution makes the most sense to me. It's a nice and simple 2D solution
where we increment the previous match in case letters coincide, or
take the max of the previous row and col if they don't.

Easy to understand.

Will need to revisit this soon, tho should be fine coding this up when i do.

---------------------

# 2025-10-17 09:47: 78. Subsets (Medium) (time: 2m 48):

```python3
class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:

        def dfs(i):
            res.append(sub[:])
            for j in range(i, len(nums)):
                sub.append(nums[j])
                dfs(j + 1)
                sub.pop()
        (sub, res) = ([], [])
        dfs(0)
        return res
```

---------------------

# 2025-10-17 09:58: 77. Combinations (Medium) (time: 4m 28):

```python3
class Solution:

    def combine(self, n: int, k: int) -> List[List[int]]:

        def dfs(i):
            if len(sub) == k:
                res.append(sub[:])
            future_choices = range(i, n)
            for j in future_choices:
                sub.append(j + 1)
                dfs(j + 1)
                sub.pop()
        (res, sub) = ([], [])
        dfs(0)
        return res
```

## notes: 

This solution is correct but suboptimial because it lacks prunine.
Revisit.

---------------------

# 2025-10-17 10:53: 90. Subsets II (Medium) (time: 29m 20):

```python3
class Solution:

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:

        def dfs(i, depth=0):
            res.append(sub[:])
            future_choices = [*range(i, len(nums))]
            if future_choices:
                prev = None
                for j in future_choices:
                    if prev == nums[j]:
                        continue
                    sub.append(nums[j])
                    dfs(j + 1, depth + 1)
                    prev = sub.pop()
        nums.sort()
        (res, sub) = ([], [])
        dfs(0)
        return res
```

## notes: 

My first thought is to add the subsets to a set, but
let's explore whether there's a more elegant way of
doing this.

So it seems that sorting the input, and pruning paths
using a `prev` variable is the right solution.

I find it a bit unintuitive that sorting works, because
i would have assumed that the subsets would have to be
interally in the same order.

Solved.

---------------------

# 2025-10-17 12:18: 39. Combination Sum (Medium) - learning (time: 23m 29):

```python3
class Solution:

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(i):
            if sum(sub) == target:
                res.add(tuple(sub[:]))
                return
            for j in range(i, len(nums)):
                sub.append(nums[j])
                dfs(j + 1)
                sub.pop()
        nums = []
        for c in candidates:
            nums.extend([c] * (target // c))
        (sub, res) = ([], set([]))
        dfs(0)
        return [list(x) for x in res]
```

## notes: 

Hmm i'm stumped by the follow constraint:

The same number may be chosen from candidates an unlimited number of times

I think doing a prefix sum might help, and check for divisibility somehow,
but this still feels a bit too advanced for now.

Basically this solution works, but it hits a TLE, so it's clearly brute force.

---------------------

# 2025-10-17 12:37: 2553. Separate the Digits in an Array (Easy) (time: 3m 12):

```python3
class Solution:

    def getDigits(self, n):
        res = []
        while n:
            res.append(n % 10)
            n //= 10
        return res[::-1]

    def separateDigits(self, nums: List[int]) -> List[int]:
        return [*chain(*[self.getDigits(x) for x in nums])]
```

---------------------

# 2025-10-17 12:49: 2744. Find Maximum Number of String Pairs (Easy) (time: 8m 37):

```python3
class Solution:

    def maximumNumberOfStringPairs(self, words: List[str]) -> int:
        inverted = [x[::-1] for x in words]
        counts = 0
        for (i, j) in combinations(range(len(words)), 2):
            counts += words[i] == inverted[j]
        return counts
```

---------------------

# 2025-10-17 13:01: 2778. Sum of Squares of Special Elements (Easy) (time: 4m 22):

```python3
class Solution:

    def sumOfSquares(self, nums: List[int]) -> int:
        return sum((nums[i - 1] * nums[i - 1] for i in range(1, len(nums) + 1) if len(nums) % i == 0))
```

---------------------

# 2025-10-17 13:53: 2678. Number of Senior Citizens (Easy) (time: 3m 44):

```python3
class Solution:

    def countSeniors(self, details: List[str]) -> int:
        return sum((age[11:13] > '60' for age in details))
```

---------------------

# 2025-10-18 09:27: 3658. GCD of Odd and Even Sums (Easy) (time: 7m 58):

```python3
class Solution:

    def gcdOfOddEvenSums(self, n: int) -> int:
        even = sum((x for x in range(2, n * 2 + 1, 2) if x % 2 == 0))
        odd = sum((x for x in range(1, n * 2 + 1, 2) if x % 2 != 0))
        return gcd(even, odd)
```

---------------------

# 2025-10-18 09:49: 3232. Find if Digit Game Can Be Won (Easy) (time: 6m 52):

```python3
class Solution:

    def canAliceWin(self, nums: List[int]) -> bool:
        sum_of_single = sum((x for x in nums if x < 10))
        sum_of_double = sum((x for x in nums if x >= 10))
        return sum_of_single != sum_of_double
```

---------------------

# 2025-10-18 09:58: 590. N-ary Tree Postorder Traversal (Easy) (time: 3m 51):

```python3
class Node:

    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

class Solution:

    def postorder(self, root: 'Node') -> List[int]:

        def dfs(node):
            if not node:
                return
            for c in node.children:
                dfs(c)
            res.append(node.val)
        res = []
        dfs(root)
        return res
```

---------------------

# 2025-10-18 10:11: 942. DI String Match (Easy) (time: 10m 48):

```python3
class Solution:

    def diStringMatch(self, s: str) -> List[int]:
        D = len(s)
        I = 0
        res = []
        for c in s + s[-1]:
            if c == 'I':
                res.append(I)
                I += 1
            else:
                res.append(D)
                D -= 1
        return res
```

---------------------

# 2025-10-18 10:17: 1636. Sort Array by Increasing Frequency (Easy) (time: 3m 34):

```python3
class Solution:

    def frequencySort(self, nums: List[int]) -> List[int]:
        c = Counter(nums)
        nums.sort(key=lambda x: [c[x], -x])
        return nums
```

---------------------

# 2025-10-18 10:28: 2697. Lexicographically Smallest Palindrome (Easy) (time: 9m 15):

```python3
class Solution:

    def makeSmallestPalindrome(self, s: str) -> str:
        s = list(s)
        n = len(s)
        for i in range(n // 2):
            (a, b) = (s[i], s[n - i - 1])
            if a < b:
                s[n - i - 1] = a
            else:
                s[i] = b
        return ''.join(s)
```

---------------------

# 2025-10-18 10:40: 1309. Decrypt String from Alphabet to Integer Mapping (Easy) - learning (time: 8m 57):

```python3
class Solution:

    def freqAlphabets(self, s: str) -> str:
        (s, res) = (list(s), '')
        while s:
            c = s.pop()
            if c == '#':
                x = s.pop() + s.pop()
                res += chr(ord('a') + int(x[::-1]) - 1)
            else:
                res += chr(ord('a') + int(c) - 1)
        return res[::-1]
```

## notes: 

Not my solution. I didn't think of using a stack.

Revisit.

---------------------

# 2025-10-18 10:45: 3550. Smallest Index With Digit Sum Equal to Index (Easy) (time: 2m 59):

```python3
class Solution:

    def smallestIndex(self, nums: List[int]) -> int:

        def digits(n):
            r = []
            while n:
                r.append(n % 10)
                n //= 10
            return r
        return next((i for (i, v) in enumerate(nums) if sum(digits(v)) == i), -1)
```

---------------------

# 2025-10-19 10:42: 728. Self Dividing Numbers (Easy) (time: 6m 5):

```python3
class Solution:

    def selfDividingNumbers(self, left: int, right: int) -> List[int]:

        def get_digits(n):
            digits = []
            while n:
                digits.append(n % 10)
                n //= 10
            return digits

        def is_divisible(n):
            return all((n % x == 0 if x != 0 else False for x in get_digits(n)))
        return [*filter(lambda x: is_divisible(x), range(left, right + 1))]
```

---------------------

# 2025-10-19 11:34: 1380. Lucky Numbers in a Matrix (Easy) (time: 10m 58):

```python3
class Solution:

    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        get_col = lambda c: [matrix[i][c] for i in range(len(matrix))]
        lucky = []
        for (i, row) in enumerate(matrix):
            _min = float('inf')
            _min_index = 0
            for (j, val) in enumerate(row):
                if val < _min:
                    _min = val
                    _min_index = j
            col = get_col(_min_index)
            _max = max(col)
            if _min == _max:
                lucky.append(_min)
        return lucky
```

---------------------

# 2025-10-19 11:43: 3005. Count Elements With Maximum Frequency (Easy) (time: 4m 10):

```python3
class Solution:

    def maxFrequencyElements(self, nums: List[int]) -> int:
        counts = Counter(nums)
        _max = max(counts.values())
        return list(counts.values()).count(_max) * _max
```

---------------------

# 2025-10-19 11:51: 1725. Number Of Rectangles That Can Form The Largest Square (Easy) (time: 4m 58):

```python3
class Solution:

    def countGoodRectangles(self, rectangles: List[List[int]]) -> int:
        mins = [min(r) for r in rectangles]
        _max = max(mins)
        return mins.count(_max)
```

---------------------

# 2025-10-19 11:58: 2710. Remove Trailing Zeros From a String (Easy) (time: 2m 26):

```python3
class Solution:

    def removeTrailingZeros(self, num: str) -> str:
        return ''.join(dropwhile(lambda x: x == '0', num[::-1]))[::-1]
```

---------------------

# 2025-10-19 12:00: 1941. Check if All Characters Have Equal Number of Occurrences (Easy) (time: 1m 7):

```python3
class Solution:

    def areOccurrencesEqual(self, s: str) -> bool:
        return len(set(Counter(s).values())) == 1
```

---------------------

# 2025-10-19 12:15: 1700. Number of Students Unable to Eat Lunch (Easy) (time: 12m 30):

```python3
class Solution:

    def countStudents(self, students: List[int], sandwiches: List[int]) -> int:
        St = deque(students)
        Sw = deque(sandwiches)
        count = 0
        while True:
            if Sw[0] == St[0]:
                count = 0
                Sw.popleft()
                St.popleft()
                if len(St) == 0 or len(Sw) == 0:
                    break
            else:
                count += 1
                St.append(St.popleft())
                if count == len(sandwiches):
                    break
        return len(St)
students = [1]
sandwiches = [0]
```

---------------------

# 2025-10-20 02:37: 1309. Decrypt String from Alphabet to Integer Mapping (Easy) (time: 8m 30):

```python3
class Solution:

    def freqAlphabets(self, s: str) -> str:
        stack = list(s)
        res = []
        while stack:
            if stack[-1] == '#':
                stack.pop()
                (a, b) = (stack.pop(), stack.pop())
                num = int(b) * 10 + int(a)
                letter = ascii_letters[num - 1]
                res.append(letter)
            else:
                a = stack.pop()
                num = int(a)
                letter = ascii_letters[num - 1]
                res.append(letter)
        return ''.join(res[::-1])
```

---------------------

# 2025-10-20 08:31: 206. Reverse Linked List (Easy) (time: 1m 23):

```python3
class Solution:

    def reverseList(self, h: Optional[ListNode]) -> Optional[ListNode]:
        d = ListNode()
        while h:
            (d.next, h.next, h) = (h, d.next, h.next)
        return d.next
```

---------------------

# 2025-10-20 11:02: 322. Coin Change (Medium) (time: 2m 22):

```python3
class Solution:

    def coinChange(self, coins, amount):
        cum_dp = [0] + [maxsize] * amount
        for coin in coins:
            for x in range(coin, amount + 1):
                cum_dp[x] = min(cum_dp[x], cum_dp[x - coin] + 1)
        return cum_dp[amount] if cum_dp[amount] != maxsize else -1
```

## notes: 

Makes a lot more sense, but should reschedule in a week or so.

---------------------

# 2025-10-20 11:20: 39. Combination Sum (Medium) (time: 10m 56):

```python3
class Solution:

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(i, combs, target):
            if target == 0:
                res.append(combs[:])
                return
            if target < 0 or i >= len(candidates):
                return
            combs.append(candidates[i])
            dfs(i, combs, target - candidates[i])
            combs.pop()
            dfs(i + 1, combs, target)
        res = []
        dfs(0, [], target)
        return res
```

## notes: 

Better, but must reschedule soon.

---------------------

# 2025-10-20 11:49: 1143. Longest Common Subsequence (Medium) (time: 8m 54):

```python3
class Solution:

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        text1 = ' ' + text1
        text2 = ' ' + text2
        dp = []
        for _ in range(len(text1)):
            dp.append([0] * len(text2))
        for i in range(len(text1)):
            for j in range(len(text2)):
                if text1[i] == text2[j]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
        return dp[-1][-1] - 1
```

---------------------

# 2025-10-20 13:15: 2716. Minimize String Length (Easy) (time: 0m 39):

```python3
class Solution:

    def minimizedStringLength(self, s: str) -> int:
        return len(set(s))
```

---------------------

# 2025-10-20 13:32: 1436. Destination City (Easy) (time: 5m 50):

```python3
class Solution:

    def destCity(self, paths: List[List[str]]) -> str:
        destination_cities = set([x[1] for x in paths])
        departure_cities = set([x[0] for x in paths])
        return next(iter(destination_cities - departure_cities))
```

---------------------

# 2025-10-20 13:41: 2427. Number of Common Factors (Easy) (time: 2m 15):

```python3
from math import gcd

class Solution:

    def commonFactors(self, a: int, b: int) -> int:
        _gcd = gcd(a, b)
        return len([x for x in range(1, _gcd + 1) if a % x == 0 and b % x == 0])
```

---------------------

# 2025-10-21 07:47: 560. Subarray Sum Equals K (Medium) (time: 2m 19):

```python3
class Solution:

    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        res = 0
        for n in nums:
            prefix += n
            c = prefix - k
            if c in D:
                res += D[c]
            D[prefix] += 1
        return res
```

---------------------

# 2025-10-21 08:03: 33. Search in Rotated Sorted Array (Medium) (time: 5m 29):

```python3
class Solution:

    def search(self, nums: List[int], target: int) -> int:
        (left, right) = (0, len(nums) - 1)
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
        return -1
```

---------------------

# 2025-10-21 08:33: 543. Diameter of Binary Tree (Easy) (time: 18m 54):

```python3
class Solution:

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:

        def dfs(node):
            if not node:
                return 0
            max_left = dfs(node.left)
            max_right = dfs(node.right)
            self.diam = max(self.diam, max_left + max_right)
            _max = max(max_left, max_right) + 1
            node.val = _max
            return _max
        self.diam = 0
        dfs(root)
        return self.diam
```

---------------------

# 2025-10-21 09:29: 98. Validate Binary Search Tree (Medium) (time: 10m 44):

```python3
class Solution:

    def isValidBST(self, root: TreeNode) -> bool:

        def dfs(node, max_bound, min_bound):
            if not node:
                return True
            node_is_valid = min_bound < node.val < max_bound
            left_is_valid = dfs(node.left, node.val, min_bound)
            right_is_valid = dfs(node.right, max_bound, node.val)
            return all([left_is_valid, right_is_valid, node_is_valid])
        return dfs(root, maxsize, -maxsize)
```

---------------------

# 2025-10-21 10:13: 105. Construct Binary Tree from Preorder and Inorder Traversal (Medium) (time: 16m 12):

```python3
class Solution:

    def buildTree(self, preorder, inorder):
        if len(preorder) == 0 or len(inorder) == 0:
            return None
        val = preorder[0]
        index = inorder.index(val)
        num_left_nodes = index
        left_tree = self.buildTree(preorder[1:num_left_nodes + 1], inorder[:index])
        right_tree = self.buildTree(preorder[1 + num_left_nodes:], inorder[num_left_nodes + 1:])
        node = TreeNode(val, left_tree, right_tree)
        return node

def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    res = []
    q = [root]
    while q:
        node = q.pop(0)
        res.append(node.val if node else None)
        if node:
            q.append(node.left)
            q.append(node.right)
    while res and res[-1] is None:
        res.pop()
    return res
```

---------------------

# 2025-10-21 11:06: 437. Path Sum III (Medium) (time: 4m 17):

```python3
from copy import copy

class Solution:

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:

        def dfs(node, prefix, D):
            if not node:
                return
            prefix += node.val
            c = prefix - targetSum
            if c in D:
                self.res += D[c]
            D[prefix] += 1
            dfs(node.left, prefix, copy(D))
            dfs(node.right, prefix, copy(D))
        D = defaultdict(int)
        D[0] = 1
        self.res = 0
        dfs(root, 0, D)
        return self.res
```

---------------------

# 2025-10-21 11:43: 1539. Kth Missing Positive Number (Easy) - learning (time: 25m 13):

```python3
class Solution:

    def findKthPositive(self, arr: List[int], k: int) -> int:
        (left, right) = (0, len(arr) - 1)
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k
```

## notes: 

Hmm i got close! but returned return arr[mid] + k - missing instead of
left + k. So will keep this as learning for now.

---------------------

# 2025-10-21 12:13: 1748. Sum of Unique Elements (Easy) (time: 1m 15):

```python3
class Solution:

    def sumOfUnique(self, nums: List[int]) -> int:
        return sum((number for (number, count) in Counter(nums).items() if count == 1))
```

---------------------

# 2025-10-21 12:35: Review Notes

Today was interesting. Similarly to yesterday.

# 33. Search in Rotated Sorted Array

This problem caused me lots of issues in the past. I guess i was looking at the code instead of thinking about the simple pattern: only searching in the sorted subarray, and switching to the other subarray if the target is not within the sorted array.

For some reason a problem that used to trip me up feels trivial now.

# 543. Diameter of Binary Tree

This solve felt good. The key insight that really helped was getting the max depth of both left and right subtrees, and tracking the global max for max left + max right depths. Again this solve feels intuitive now.

# 98. Validate Binary Search Tree

This also feels obvious now. To valide the full binary tree, one needs to validate each subtree, which involves passing new bounds as we recurse into the subtrees. Obvious with hindsight.

# 105. Construct Binary Tree from Preorder and Inorder Traversal

The intuition felt easy this time around. Writing the array vals on the ipad, and colouring matching subarrays makes the pattern jump out. Using recursion for those subarrays feels quite trivial now.

# 437. Path Sum III

Another problem that feels trivial now. It feels like i've deeply imprinted the pattern for subarray sum equals k, so applying it to a tree felt entirely trivial.

# Kth Missing Positive Number

Again this solve involved writing the array values on the ipad, with the missing values in a different colour, and the indices in a third colour, then observing how to leverage the various values. Computing the number of missing values up to was trivial, however i hesitated with e.g left < right versus left <= right, then i didn't spot that i needed to use the left pointer instead of mid on the return.

# 1748. Sum of Unique Elements

Easy / trivial question using a Counter and functional python.

---

I'm seeing how beneficial it is tackling my 'learning' queue. It feels daunting before jumping back into a learning item, but many quickly turned out to be trivial to solve now.

I'm also considering adding the 'study' of a hard question daily. So picking a hard question, studying the question, then studying a variety of solutions. Hopefully i'll get started with that tomorrow.

---------------------

# 2025-10-22 07:30: Review Notes

# 15. 3Sum

Another problem i struggled with multiple times, despite the solution be quite straight forward.

```python
class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set()
        n = len(nums)

        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            seen = set()
            target = -nums[i]
            for j in range(i + 1, n):
                complement = target - nums[j]
                if complement in seen:
                    res.add((nums[i], complement, nums[j]))
                seen.add(nums[j])

        return [list(t) for t in sorted(res)]
```

# 974. Subarray Sums Divisible by K

I struggled with the intuition for this one initially. However this solution elucidates things a little bit.

```python
class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        D = defaultdict(int)
        D[0] = 1
        prefix_sum = 0
        res = 0
        for n in nums:
            prefix_sum += n
            prefix_mod = prefix_sum % k
            res += D[prefix_mod]
            D[prefix_mod] += 1
        return res
```

We accumulate `n` into `prefix_sum` because `subarray_sum = prefix[j] - prefix[i - 1]`.

Since we want:

`subarray_sum % k == 0`

We can substitute the formula:

`(prefix[j] - prefix[i - 1]) % k == 0`

Which is equivalent to:

`prefix[j] % k == prefix[i - 1] % k`

> The sum of the subarray between i and j is divisible by k if and only if the prefix sums at j and i - 1 leave the same remainder when divided by k.

# 287. Find the Duplicate Number

```python
class Solution(object):
    def findDuplicate(self, nums):
        # not my solution
        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow
```

---------------------

# 2025-10-22 09:33: 2960. Count Tested Devices After Test Operations (Easy) (time: 5m 41):

```python3
class Solution:

    def countTestedDevices(self, batteryPercentages: List[int]) -> int:
        tested = 0
        for i in range(len(batteryPercentages)):
            bat = batteryPercentages[i]
            if bat > 0:
                tested += 1
                for j in range(i + 1, len(batteryPercentages)):
                    batteryPercentages[j] = max(batteryPercentages[j] - 1, 0)
        return tested
```

---------------------

# 2025-10-22 10:27: 518. Coin Change II (Medium) - learning (time: 36m 53):

```python3
class Solution:

    def change(self, amount: int, coins: List[int]) -> int:
        """
        Not my solution
        https://leetcode.com/problems/coin-change-ii/solutions/3892702/100-dynamic-programming-video-optimal-solution/
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for j in range(coin, amount + 1):
                dp[j] += dp[j - coin]
        return dp[amount]
```

## notes: 

Hmm it still feels like i'm warming up to DP and the coin change problem, so this
extra twist of counting combos feels a bit of a stretch. For sure i can count
the combinations by simply computing all the subsets equal to amount, with repeats
however there are too many combinations, so this approach won't be efficient.

Let's try and think through this example

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

So one approach here is to sort the coins, to start with small denomiations,
in the case of 1, it gives us 1 way of adding up to 5.

In the case of 2, we're taking the number of ways for `1`, and subtracting 2, which is
another way, then 4, which is yet another way.

In the case of 5, it's already our target amount, so cannot compute combinations.

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        coins.sort()

        @cache
        def dp(coinIndex, amount):
            if amount == 0:
                return 0
            val = coins[coinIndex]
            if coins[coinIndex] == 1:
                return 1
            div, mod = divmod(amount, val)
            ways = 1
            if div:
                for i in range(1, div + 1):
                    ways += dp(coinIndex - 1, amount - (val * i))
            return ways

        _5 = dp(2, amount)
        return _5

Out of time. I give up. Will have to look up the solution.

---------------------

# 2025-10-22 11:42: 416. Partition Equal Subset Sum (Medium) (time: 32m 34):

```python3
class Solution:

    def canPartitionBruteForce(self, nums: List[int]) -> bool:
        """
        This solution isn't very efficient, as we're recompute the sum for
        each combination.
        """
        n = sum(nums)
        if n % 2:
            return False
        combs = chain(*(combinations(nums, x) for x in range(1, len(nums) + 1)))
        return any((sum(comb) == n // 2 for comb in combs))

    def canPartitionsubsets(self, nums: List[int]) -> bool:
        """
        This time around, we generate subsets manually, and check if
        their sub is half of n, not super efficient, but can build on
        this.
        """
        n = sum(nums)
        if n % 2:
            return False

        def subsets(i, subset):
            if sum(subset) == n // 2:
                return True
            for j in range(i, len(nums)):
                if subsets(j + 1, subset + [nums[i]]):
                    return True
            return False
        return subsets(0, [])

    def canPartition(self, nums: List[int]) -> bool:
        """
        Optimal solution:
        - Compute subsets
            - Compute prefix
            - if prefix sum is double sum of nums, return True
        """
        n = sum(nums)
        if n % 2:
            return False

        @cache
        def subsets(i, prefix):
            if prefix == n // 2:
                return True
            if prefix > n // 2:
                return False
            for j in range(i, len(nums)):
                r = subsets(j + 1, prefix + nums[j])
                if r == True:
                    return True
            return False
        nums.sort(reverse=True)
        return subsets(0, 0)
```

## notes: 

Ok so the trick here is to generate a subset that's equal to half the sum of nums.
So already, we if the sum is not divisible by 2, then it's not possible.

There are multiple approaches here, but this most efficient might be
to generate subsets with a prefix.

Apparently not. This hits a TLE.

Ok finally passed after several submissions to overcome TLEs.

Would be good to revisit this, with the most optimal solution.

---------------------

# 2025-10-22 18:57: 2810. Faulty Keyboard (Easy) (time: 7m 30):

```python3
class Solution:

    def finalString(self, s: str) -> str:
        s = list(s)
        for (i, c) in enumerate(s):
            if c == 'i':
                s[:i] = s[:i][::-1]
        return ''.join([x for x in s if x != 'i'])
```

---------------------

# 2025-10-22 19:21: 682. Baseball Game (Easy) (time: 11m 33):

```python3
class Solution:

    def calPoints(self, ops: List[str]) -> int:

        def is_digit(x):
            try:
                if int(x):
                    return True
            except:
                return False
        score = []
        for (i, o) in enumerate(ops):
            if is_digit(o):
                score.append(int(o))
            elif o == '+':
                score.append(score[-1] + score[-2])
            elif o == 'D':
                score.append(score[-1] * 2)
            elif o == 'C':
                score.pop()
        return sum(score)
```

---------------------

# 2025-10-22 19:54: 139. Word Break (Medium) (time: 22m 18):

```python3
class Solution:

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        @cache
        def dp(i):
            if len(s) == i:
                return True
            for w in wordDict:
                if s[i:].startswith(w):
                    if dp(i + len(w)):
                        return True
            return False
        s_letters = set(s)
        words_letters = set(chain(*wordDict))
        if s_letters - words_letters != set([]):
            return False
        wordDict.sort(key=len, reverse=True)
        return dp(0)
```

## notes: 

This is likely a backtracking problem.
We iterate over all the words, and check if s starts
with the word. If it does, we explore the rest of the string
(doing the same). If no words match we backtrack.

Ok this seems to work, but i've hit a TLE. So a couple of optimizations
are:

- use indices instead of substrings
- sort wordDict by reverse length

Solved!

---------------------

# 2025-10-22 20:45: 40. Combination Sum II (Medium) - learning (time: 28m 7):

```python3
class Solution:

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(i, prefix):
            if prefix == target:
                res.add(tuple(subset[:]))
                return False
            if prefix > target:
                return -1
            prev = None
            for j in range(i, len(candidates)):
                subset.append(candidates[j])
                r = dfs(j + 1, prefix + candidates[j])
                subset.pop()
                if r == False:
                    if prev == candidates[j]:
                        break
                prev = candidates[j]
                if r == -1:
                    break
            return True
        candidates.sort()
        res = set([])
        subset = []
        dfs(0, 0)
        return [list(x) for x in res]
```

## notes: 

An approach might be to generate all subsets, and checking if their
sum equals target.

To avoid duplicates subsets, we put them in a set.

I'll do that as a first pass, then optimize.

Great so seems to work, but we hit a TLE on long inputs, so a prefix
optimization is likely required, also better pruning, i.e
if the prefix is greater than target, no more need to explore.

Well sadly i'm still hitting a TLE when many repeats, and i'm running
out of time to solve this question. I'll mark it as 'learning'
and go through the logic carefully before re-attempting,
to better understand pruning for the repeats.

Reschedule.

---------------------

# 2025-10-22 21:20: 518. Coin Change II (Medium) (time: 5m 44):

```python3
class Solution:

    def change(self, amount: int, coins: List[int]) -> int:
        DP = [1] + [0] * amount
        coins.sort()
        for coin in coins:
            for i in range(coin, amount + 1):
                DP[i] += DP[i - coin]
        return DP[-1]
```

## notes: 

I remembered the solution since this question was scheduled earlier today.
Can't say i've yet established a deep intuition as to why this works.

---------------------

# 2025-10-22 22:11: 46. Permutations (Medium) - learning (time: 29m 59):

```python3
class Solution:

    def permute(self, nums: List[int]) -> List[List[int]]:

        def swap(i, j, nums):
            (nums[i], nums[j]) = (nums[j], nums[i])
            r = nums[:]
            (nums[i], nums[j]) = (nums[j], nums[i])
            return r
        res = []
        for k in range(len(nums)):
            for (i, j) in combinations(range(len(nums[k:])), 2):
                res.append(nums[:k] + swap(i, j, nums[k:]))
        return res
```

## notes: 

Interesting problem!

Can't really think of a solution, so will just
experiment with subset generation as a base, and
try swapping elements instead of skipping them.

Hmm i give up. This is as close as i got.

---------------------

# 2025-10-22 22:20: 965. Univalued Binary Tree (Easy) (time: 3m 50):

```python3
class Solution:

    def isUnivalTree(self, root: Optional[TreeNode]) -> bool:

        def dfs(node):
            if not node:
                return True
            if not vals:
                vals.add(node.val)
            elif node.val not in vals:
                return False
            return dfs(node.left) and dfs(node.right)
        vals = set([])
        return dfs(root)
```

---------------------

# 2025-10-23 09:28: 15. 3Sum (Medium) - learning (time: 18m 20):

```python3
class Solution:

    def twoSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        D = defaultdict(int)
        D[0] = 1
        target = 0
        for j in range(len(nums)):
            complement = target - nums[j]
            if complement in D:
                res.append([complement, nums[j]])
                D[complement] += 1
            D[nums[j]] += 1
        return res

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set([])
        D = set()
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            target = -nums[i]
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in D:
                    res.add((nums[i], complement, nums[j]))
                D.add(nums[j])
        return [list(x) for x in sorted(res)]
```

## notes: 

I'm not sure why, but i had to peek at the solution for this. Clearly something
isn't sticking, so let's go over this step by step.

First of all, we sort nums. I'm guessing this is because we want to avoid duplicate
triplets, but i'm not 100% sure about that.

We use a set for our result, and a set to track what has been seen.

We start with an i iterator over the entire list.

 i
[1, -1, 0, 5, -5]

if i > 0 and nums[i] == nums[i - 1]:
    continue

I think this is to skip over the possibility of duplicate triplets, but will
have to confirm if this is really needed.

Next, the target is -nums[i], which makes sense, because we're now performing
a two sum, and that's our target.

Next we iterate from i + 1 to the len of nums, which also makes sense.

Our complement is: complement = target - nums[j] which also makes sense.

 i   j
[1, -1, 0, 5, -5]

complement = -1 - (-1)
i.e 0

The complement is minus i, and if we take away what's at j, we get 0,
meaning if we encouter 0 we'll have a triplet.

So if the complement is in d, we add the triplet to res.

Finally we add nums[j] to our seen set, for our complement matching
later.

Reschedule.

---------------------

# 2025-10-23 09:49: 974. Subarray Sums Divisible by K (Medium) (time: 18m 25):

```python3
class Solution:

    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        res = 0
        for n in nums:
            prefix += n
            complement = prefix % k
            if complement in D:
                res += D[complement]
            D[prefix % k] += 1
        return res
```

## notes: 

I actually stepped through this solution very carefully yesterday, and the
pattern clicked so let's hope i can summon it up again.

It really helped to just treat this as a subarray sum equals k first.

Ok i had to look up subarray sum equals k. I guess i got confused after 3 sum, because
the pattern is somewhat similar, but not.

With subarray sum equals k, the complement is `prefix - k`, and we need to initialize
the dict with D[0] = 1.

Now to transform this into a subarray sum divisible by k, we need to think of the properties
of modulor arithmetic, and how they jive with the subarray sum problem.

In the subarray sum problem, the sum of the range i to j is prefix[j] - prefix[i - 1].
In our case we want to check for divisibility, i.e:

(prefix[j] - prefix[i - 1]) % k = 0

Using modulo arithmetic:

prefix[j] % k - prefix[i - 1] % k  = 0

prefix[j] % k = prefix[i - 1] % k

Hmm ok i think this passes.. but i'll need to revisit this soon, still on a learning basis.

---------------------

# 2025-10-23 10:29: 40. Combination Sum II (Medium) (time: 3m 45):

```python3
class Solution:

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        def dfs(i, prefix=0):
            if prefix == target:
                res.append([*sorted(subset[:])])
                return
            prev = None
            for j in range(i, len(candidates)):
                if candidates[j] == prev:
                    continue
                prev = candidates[j]
                if prefix + candidates[j] <= target:
                    subset.append(candidates[j])
                    dfs(j + 1, prefix + candidates[j])
                    subset.pop()
        candidates.sort()
        res = []
        subset = []
        dfs(0)
        return [x for x in sorted(res)]
```

---------------------

# 2025-10-23 10:48: 15. 3Sum (Medium) - learning (time: 11m 16):

```python3
class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set()
        seen = set()
        nums.sort()
        for i in range(len(nums)):
            if i > 0 and nums[i - 1] == nums[i]:
                continue
            target = -nums[i]
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in seen:
                    res.add(tuple(sorted((nums[i], nums[j], complement))))
                seen.add(nums[j])
        return [list(x) for x in sorted(res)]
```

## notes: 

Botched this again... i forgot to sort, so got confused why there were some repeats.

Mildly annoying.

---------------------

# 2025-10-23 11:15: 621. Task Scheduler (Medium) - learning (time: 17m 2):

```python3
class Solution:

    def leastInterval(self, tasks: List[str], n: int) -> int:
        max_heap = [-x for x in Counter(tasks).values()]
        heapify(max_heap)
        cooloff = deque()
        time = 0
        while max_heap or cooloff:
            time += 1
            while cooloff and cooloff[0][0] < time:
                (t, count) = cooloff.popleft()
                heappush(max_heap, -count)
            if max_heap:
                count = -heappop(max_heap) - 1
                if count > 0:
                    cooloff.append((time + n, count))
        return time
```

## notes: 

Got a bit further, but still had to cheat and glance at the solution.

My main area of confusion was transferring the task from the cooloff
deque back onto the max heap.. which makes total sense, but for some
reason it evaded me.

Also i was decrementing the counter after the check `if count > 0`
instead of before.

I'll keep this in learning for now.

---------------------

# 2025-10-23 11:42: 15. 3Sum (Medium) - learning (time: 11m 43):

```python3
class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set()
        for i in range(len(nums)):
            seen = set()
            target = -nums[i]
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in range(i + 1, len(nums)):
                complement = target - nums[j]
                if complement in seen:
                    res.add(tuple(sorted([nums[i], nums[j], complement])))
                seen.add(nums[j])
        return [list(x) for x in res]
```

## notes: 

Still managed to come short... `seen` needs to be inside the inner loop.

This is frustrating.

Keeping on the learning stack.

---------------------

# 2025-10-23 12:07: 621. Task Scheduler (Medium) (time: 7m 25):

```python3
class Solution:

    def leastInterval(self, tasks: List[str], n: int) -> int:
        max_heap = [-x for x in Counter(tasks).values()]
        heapify(max_heap)
        cooloff = deque()
        time = 0
        while max_heap or cooloff:
            time += 1
            while cooloff and cooloff[0][0] < time:
                heappush(max_heap, cooloff.pop()[1])
            if max_heap:
                remaining = -heappop(max_heap) - 1
                if remaining > 0:
                    cooloff.append((time + n, -remaining))
        return time
```

## notes: 

This took many attempts, to the point where it now feels like spaced repetition
versus real solving.

That being said, this simulation is really neat, i.e moving tasks back and
forth between a heap and a deque, cleanly.

Feels useful, and it would be interesting covering variations of this pattern.

---------------------

# 2025-10-23 12:25: 15. 3Sum (Medium) (time: 5m 30):

```python3
class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set()
        for i in range(len(nums)):
            if i > 0 and nums[i - 1] == nums[i]:
                continue
            target = -nums[i]
            seen = set()
            for j in range(i + 1, len(nums)):
                c = target - nums[j]
                if c in seen:
                    res.add(tuple(sorted((nums[i], nums[j], c))))
                seen.add(nums[j])
        return [list(x) for x in sorted(list(res))]
```

## notes: 

Finally solved. But this took many repetitions.

---------------------

# 2025-10-23 14:54: 1252. Cells with Odd Values in a Matrix (Easy) (time: 8m 4):

```python3
class Solution:

    def oddCells(self, m: int, n: int, indices: List[List[int]]) -> int:
        mat = [[0] * n for _ in range(m)]

        def incr_row(row):
            for i in range(n):
                mat[row][i] += 1

        def incr_col(col):
            for i in range(m):
                mat[i][col] += 1
        for ind in indices:
            incr_row(ind[0])
            incr_col(ind[1])
        return sum((x % 2 != 0 for x in chain(*mat)))
```

---------------------

# 2025-10-23 14:58: 1979. Find Greatest Common Divisor of Array (Easy) (time: 0m 37):

```python3
from math import gcd

class Solution:

    def findGCD(self, nums: List[int]) -> int:
        return gcd(min(nums), max(nums))
```

---------------------

# 2025-10-23 15:08: 2094. Finding 3-Digit Even Numbers (Easy) - learning (time: 6m 39):

```python3
class Solution:

    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        perms = set((int(''.join((str(y) for y in x))) for x in permutations(set(digits), 3) if x[0] != 0))
        return [x for x in sorted(perms) if x % 2 == 0]
```

---------------------

# 2025-10-23 15:14: 1704. Determine if String Halves Are Alike (Easy) (time: 2m 14):

```python3
class Solution:

    def halvesAreAlike(self, s: str) -> bool:
        vowels = set('aeiou')
        s = s.lower()
        a = s[:len(s) // 2]
        b = s[len(s) // 2:]
        return sum((x in vowels for x in a)) == sum((x in vowels for x in b))
```

---------------------

# 2025-10-25 09:12: 91. Decode Ways (Medium) - learning (time: 39m 33):

```python3
class Solution:

    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n + 1):
            one_digit = int(s[i - 1:i])
            two_digits = int(s[i - 2:i])
            if one_digit != 0:
                dp[i] += dp[i - 1]
            if 10 <= two_digits <= 26:
                dp[i] += dp[i - 2]
        return dp[n]
```

## notes: 

Alright i spent a bit of time trying to solve this, but realize
i'm still fuzzy on the correct approach, so am better off going
back to learning mode on this one.

My incorrect solution:


class Solution:

    def numDecodings(self, s: str) -> int:
        DP = [1] + [0] * len(s)
        for i in range(2, len(s) + 2):
            one_digit = int(s[i - 1 : i])
            two_digits = int(s[i - 2 : i])

            if one_digit < 10:
                DP[i] = DP[i - 1] + 1

            if 10 <= two_digits <= 26:
                DP[i] = DP[i - 1] + 1

        return DP[-1]

In the correct solution we start by checking if the string starts with 0.
If it does, then there is no valid encoding.

For 12, we then declare a DP table of:

DP = [1, 1, 0]

This seems kind of aribrary.

We then start iterating with `for i in range(2, n + 1)` which
also feels arbitrary..

one_digit = int(s[i - 1 : i])
two_digits = int(s[i - 2 : i])

This sort of makes sense, but not really, because `one_digit`
turns out to be `2` and `two_digits` turns out to be `12`.

So we never explored the possibility of `one_digit` being `1` which
is confusing.

if one_digit != 0:
    dp[i] += dp[i - 1]

Why are we checking for one_digit not being zero? I guess this makes
sense as we can have for example 10, in which case we'd have the letters
A and J, and the 0 would be skipped.

In the correct solution we also do:

if 10 <= two_digits <= 26:
    dp[i] += dp[i - 2]

Which kind of makes sense but dp[i] += dp[i - 2] also feels arbitrary.

Time to ask an LLM about my confusions:

Excellent — this is one of those classic dynamic programming (DP) problems that feels weirdly arbitrary at first, but once you understand what each dp[i] actually means, it all clicks into place. Let's go step by step and make every line intuitive.

⸻

🧩 The Core Idea

We want dp[i] to represent:

The number of ways to decode the first i characters of the string s.

That means:
        •       dp[0] → number of ways to decode the empty prefix (””), which is 1 (there's exactly one way: do nothing).
        •       dp[1] → number of ways to decode the first 1 character, e.g., "1" → A.

This is our base case.

⸻

🧠 Why dp = [1, 1, 0, …]

Let's say s = "12".
Then n = 2, and we make a dp array of size n + 1 = 3.

Index:   0  1  2
Meaning: "" "1" "12"

We initialize:

dp[0] = 1  # one way to decode an empty string
dp[1] = 1  # one way to decode the first char, as long as it's not "0"

That's why it “feels arbitrary” — but it's actually defining the meaning of dp[i] as “up to i characters.”

⸻

🔍 The Loop: for i in range(2, n + 1)

We start from i = 2 because the first two base cases are known:
        •       dp[0] for the empty string,
        •       dp[1] for the first character.

From here on, for each position i, we look back one step and two steps to see if we can decode either one or two digits ending at position i.

⸻

🔢 These two lines are the heart of it

one_digit = int(s[i - 1 : i])
two_digits = int(s[i - 2 : i])

Example: "12"

i       Substring       one_digit       two_digits
2       "12"    "2"     "12"

✅ We don't see "1" at this step because "1" was already handled when i = 1.
Each iteration's job is only to look at the “ending” of the substring up to position i.

⸻

🧮 Why the conditions

if one_digit != 0:
    dp[i] += dp[i - 1]

If the current single digit isn't "0", then you can decode it as one character.
So the number of ways to decode up to i includes all ways to decode up to i - 1, extended by this one new letter.

Example:
        •       "12": you can decode "1" (A), then "2" (B), so dp[2] gets dp[1].

⸻


if 10 <= two_digits <= 26:
    dp[i] += dp[i - 2]

If the last two digits form a valid letter (10 → J, …, 26 → Z),
then we can decode them together.
In that case, the number of new decodings we gain is equal to all the ways to decode up to i - 2.

Example:
        •       "12": "12" → L, so dp[2] += dp[0] (1).

⸻

🧩 Intuition in Action

Let's simulate s = "12":

i       s[:i]   one_digit       two_digits      dp[i]   Explanation
0       “”      —       —       1       base
1       “1”     “1”     —       1       “A”
2       “12”    “2”     “12”    dp[1] + dp[0] = 1 + 1 = 2       “AB”, “L”

✅ Output = dp[2] = 2

⸻

🔄 Another Example: s = "226"

i       s[:i]   one_digit       two_digits      dp[i]   Reason
0       “”      —       —       1       base
1       “2”     2       —       1       “B”
2       “22”    2       22      2       “BB”, “V”
3       “226”   6       26      dp[2] + dp[1] = 2 + 1 = 3       “BZ”, “VF”, “BBF”

✅ Output = 3

⸻

🚫 Why Check for "0"

A '0' cannot stand alone — there's no mapping for "0".
So if one_digit == 0, skip it.

However, "10" and "20" are valid (J and T),
which is why the second condition checks for 10 <= two_digits <= 26.

⸻

🧩 Summary of Logic

Concept Meaning
dp[i]   number of ways to decode the first i characters
dp[0] = 1       empty string base case
dp[1] = 1 if s[0] != '0' else 0 can decode the first char
one_digit       last single digit at position i-1
two_digits      last two digits ending at position i-1
Update rules    add dp[i - 1] if one_digit valid; add dp[i - 2] if two_digits valid


⸻

🧠 TL;DR Mental Model

You're standing at the end of the string.
At each step i, you can:
        •       Take 1 step back if the single digit is valid.
        •       Take 2 steps back if the last two digits form a valid code.

So the recurrence is:

dp[i] = (one_digit_valid ? dp[i-1] : 0) + (two_digits_valid ? dp[i-2] : 0)

That's the entire decoding problem distilled into one clean line.

⸻

OK i'll keep this problem in the learning queue for now.

Next attempt, i'll try this backtracking approach as it seems
more intuitive:

class Solution:
    def numDecodings(self, s: str) -> int:
        @cache
        def dfs(i):
            if i == len(s):           # reached end successfully
                return 1
            if s[i] == '0':           # invalid path
                return 0

            res = dfs(i + 1)          # take one digit

            if i + 1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
                res += dfs(i + 2)     # take two digits

            return res

        return dfs(0)

---------------------

# 2025-10-25 09:54: 2325. Decode the Message (Easy) (time: 9m 44):

```python3
class Solution:

    def decodeMessage(self, key: str, message: str) -> str:
        lut = {}
        for c in key:
            if c != ' ' and c not in lut:
                lut[c] = ascii_lowercase[len(lut)]
        lut[' '] = ' '
        return ''.join((lut[c] for c in message))
```

---------------------

# 2025-10-25 10:44: 287. Find the Duplicate Number (Medium) - learning (time: 23m 3):

```python3
class Solution(object):

    def findDuplicate(self, nums):
        slow = 0
        fast = 0
        for _ in range(len(nums) * 2):
            slow = nums[slow]
            fast = nums[nums[fast]]
```

## notes: 

Ok this question is quite.. "interesting" (feels contrived, but anyway). The idea here
is that we can use cycle detection.. because we can use the values as indices.

nums =  [1,3,4,2,2]
indices: 0,1,2,3,4

1 -> 3 -> 2 -> 4
          |   |
          ^ <-v

So value 1 we jump to the value at index 1, which is 3
at 3 we jump at value at index 3 which is 2
etc.

We notice a cycle at values `2`.

The second example isn't as simple:

nums = [3,1,3,4,2]
indices 0,1,2,3,4

3 -> 4 -> 2 -> 3
     |         |
     ^ <------ v


Ok we can see the cycle here:


def findDuplicate(self, nums):
    it = 0
    for _ in range(len(nums) + 2):
        it = nums[it]
        # print(f"{it} -> ", end="")
    # print("")
    # 1 -> 3 -> 2 -> 4 -> 2 -> 4 ->

So that's our slow pointer.

[1, 3, 4, 2, 2]
1 -> 3 -> 2 -> 4 ->
slow and fast are, 4, 4

[3, 1, 3, 4, 2]
3 -> 4 -> 2 ->
slow and fast are, 2, 2

OK i give up. I'm not sure how to init the slow and fast pointers.
I try to draw what i think is supposed to happen, but somehow it doesn't.

---------------------

# 2025-10-25 11:00: 2363. Merge Similar Items (Easy) (time: 4m 53):

```python3
class Solution:

    def mergeSimilarItems(self, items1: List[List[int]], items2: List[List[int]]) -> List[List[int]]:
        ret = defaultdict(int)
        for (value, weight) in chain(items1, items2):
            ret[value] += weight
        return [list(x) for x in sorted(ret.items(), key=lambda x: x[0])]
```

---------------------

# 2025-10-25 11:42: 24. Swap Nodes in Pairs (Medium) (time: 18m 30):

```python3
class Solution:

    def swapPairs(self, head: ListNode) -> ListNode:
        if head is None or head.next is None:
            return head
        tmp = head.next.next
        new_head = head.next
        new_head.next = head
        head.next = tmp
        if tmp:
            head.next = self.swapPairs(tmp)
        return new_head
```

---------------------

# 2025-10-25 14:07: 82. Remove Duplicates from Sorted List II (Medium) (time: 17m 28):

```python3
class Solution:

    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        remove = set()
        it = head
        prev_val = None
        while it:
            if it.val == prev_val:
                remove.add(it.val)
            prev_val = it.val
            it = it.next

        def get_non_duplicates(head):
            if not head:
                return
            while head and head.val in remove:
                head = head.next
            return head
        dh = ListNode(-1)
        it = head
        while True:
            it = get_non_duplicates(it)
            if it:
                if dh.next is None:
                    dh.next = it
                it.next = get_non_duplicates(it.next)
                it = it.next
            else:
                break
        return dh.next
```

---------------------

# 2025-10-25 15:06: 92. Reverse Linked List II (Medium) (time: 20m 52):

```python3
class Solution:

    def reverseSubList(self, head):
        d = ListNode(-1)
        tail = head
        while head:
            (d.next, head.next, head) = (head, d.next, head.next)
        return (d.next, tail)

    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if left == right:
            return head
        d = ListNode(-1, head)
        sub_start = d
        for _ in range(1, left):
            sub_start = sub_start.next
        sub_end = head
        for _ in range(1, right - 1):
            sub_end = sub_end.next
        tail = sub_end.next
        after = tail.next if tail else None
        if tail:
            tail.next = None
        (sub_start.next, sub_end) = self.reverseSubList(sub_start.next)
        if sub_end:
            sub_end.next = after
        return d.next
```

---------------------

# 2025-10-25 16:29: 941. Valid Mountain Array (Easy) (time: 27m 50):

```python3
class Solution:

    def validMountainArray(self, arr: List[int]) -> bool:
        n = len(arr)
        if n < 3:
            return False
        peak_from_left = None
        for (i, v) in enumerate(arr):
            if i == 0 or (i > 0 and arr[i - 1] < arr[i]):
                peak_from_left = (i, v)
            else:
                break
        for i in range(len(arr) - 1, -1, -1):
            if i == n - 1 or (i < n - 1 and arr[i] > arr[i + 1]):
                peak_from_right = (i, arr[i])
            else:
                break
        return peak_from_left == peak_from_right and peak_from_left[0] != n - 1 and (peak_from_right[0] != 0)
```

## notes: 

Tried to use binary search, however it seems this can't be done
faster than O(n).

Saw a discussion about using max.., then effectively two pointers
outwards from there. Seems good but not as optimal as can be.

The most optimal is to check for strictly increasing, then we no longer
strictly increasing start expecting strictly decreasing.

---------------------

# 2025-10-25 16:57: 767. Reorganize String (Medium) (time: 21m 25):

```python3
class Solution:

    def reorganizeString(self, S):
        counts = [(-count, letter) for (letter, count) in Counter(S).items()]
        heapify(counts)
        prev = None
        res = ''
        while counts:
            (count, letter) = heappop(counts)
            if letter == prev:
                if counts:
                    (count1, letter1) = heappop(counts)
                    res += letter1
                    count1 += 1
                    if count1 < 0:
                        heappush(counts, (count1, letter1))
                    prev = letter1
                    heappush(counts, (count, letter))
                else:
                    return ''
            else:
                res += letter
                count += 1
                if count < 0:
                    heappush(counts, (count, letter))
                prev = letter
        return res
```

---------------------

# 2025-10-26 04:54: 91. Decode Ways (Medium) - learning (time: 39m 28):

```python3
class Solution:

    def numDecodings(self, s: str) -> int:

        @cache
        def dfs(i):
            if i == len(s):
                return 1
            if s[i] == '0':
                return 0
            ways = dfs(i + 1)
            if i + 1 < len(s) and '10' <= s[i:i + 2] <= '26':
                ways += dfs(i + 2)
            return ways
        return dfs(0)
```

## notes: 

I've been struggling with this problem. Previously i was focussing on the bottom up tabular
solution, which may have been a bit too advanced. So will try recursive backtracking this time.

Ok i fumbled this one again. I got as far as building the correct structure, with dfs
and backtracking, but on two digits.

Maybe it'll make more sense starting from the end of the string?

Not my solution. Keeping in learning mode. Will revisit later.

---------------------

# 2025-10-26 05:09: 287. Find the Duplicate Number (Medium) - learning (time: 6m 50):

```python3
class Solution(object):

    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[fast]
            if slow == fast:
                break
```

## notes: 

Keeping this in learning mode.

---------------------

# 2025-10-26 05:41: 2094. Finding 3-Digit Even Numbers (Easy) (time: 11m 41):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        counts = dict(Counter(digits))
        res = []
        for i in range(100, 1000):
            if i % 2 == 0:
                digits = self.getDigits(i)
                digitsd = dict(Counter(digits))
                if all((digitsd[d] <= counts.get(d, -1) for d in digitsd)):
                    res.append(i)
        return res
```

## notes: 

The hint is really helpful here: The range of possible answers includes all even numbers between 100 and 999 inclusive.
Could you check each possible answer to see if it could be formed from the digits in the array?

As someone noted in a discussion thread, this question is really brilliant because most people
will come at this from a brute force angle, but the hint forces you to flip your thinking.

I'm really fascinated by these leaps in thinking, and would like to think more about how to
be more systematic about those leaps.

The process here was, instead of thinking "i have this input, and how do turn it into the output"
instead think "this output is within this range. how can i filter it it to make sure it lies
within the input set".

It reminds me of the prime sieve algorithm in this sense.

---------------------

# 2025-10-26 06:21: 1539. Kth Missing Positive Number (Easy) - learning (time: 21m 42):

```python3
class Solution:

    def findKthPositive(self, arr: List[int], k: int) -> int:
        (left, right) = (0, len(arr) - 1)
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k
```

## notes: 

Missed it again! The result is just `left + k`. I keep stumbling there.

---------------------

# 2025-10-26 06:28: 2527. Find Xor-Beauty of Array (Medium) (time: 0m 55):

```python3
class Solution:

    def xorBeauty(self, nums: List[int]) -> int:
        return reduce(xor, nums)
```

## notes: 

Remembered the solution. The proof is non trivial.

---------------------

# 2025-10-26 12:55: 287. Find the Duplicate Number (Medium) (time: 2m 1):

```python3
class Solution(object):

    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

## notes: 

Solved from memory.

---------------------

# 2025-10-26 13:16: 1283. Find the Smallest Divisor Given a Threshold (Medium) (time: 4m 17):

```python3
class Solution:

    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        low = 1
        high = sum(nums)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            condition = sum([ceil(x / mid) for x in nums])
            if condition <= threshold:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

Super easy thanks to bs minimization template.

---------------------

# 2025-10-26 14:15: 1482. Minimum Number of Days to Make m Bouquets (Medium) (time: 31m 26):

```python3
class Solution:

    def canMakeBouquet(self, bloomDay, days, m, k):
        g = [len([*b]) // k for (a, b) in groupby(bloomDay, key=lambda x: x <= days) if a]
        return sum(g)

    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        low = 1
        high = max(bloomDay)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            num_bouquets = self.canMakeBouquet(bloomDay, mid, m, k)
            if num_bouquets >= m:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

ok it's making sense now.. this likely involves minimizing the max element on a cluster.

We need to partition the array into m sets of adjacent values of size k, while minimizing the
max value found in any of those sets.

I'm wondering how this is a binary search problem... because it can be treated as an array
partitioning problem.

[(7,7,7),7,(12,7,7)]

bloomDay

---------------------

# 2025-10-26 14:51: 410. Split Array Largest Sum (Hard) - learning (time: 21m 32):

```python3
class Solution:

    def splitArray(self, nums: List[int], k: int) -> int:
        pass
```

## notes: 

ok here's a strategy: look for a subarray that matches
a certain number (guess), e.g 18.

[7,2,5,(10,8)]

Can we then split the remainder of the array (7,2,5) into k -1
adjacent sets.

If we guess 10:

[(7,2,5),(10),(8)] but we have 3 subarrays, which is too many.

If we guess 5:

[7,2,(5),10,8] now we still have at least 3 subarrays, which is too many.

If we guess 15:

[(7,2,5),(10,8)]


Ugh! I give up. This is too hard. I'm thinking of prefix sum solutions,
binary search etc. but it might be a bit too early still for such
a hard question. Soon though.

---------------------

# 2025-10-26 15:14: 1552. Magnetic Force Between Two Balls (Medium) - learning (time: 6m 15):

```python3
class Solution:

    def maxDistance(self, position: List[int], m: int) -> int:
        pass
```

## notes: 

I appreciate being pushed into the deep end like this, but
this still feels hard.

---------------------

# 2025-10-26 15:17: 1539. Kth Missing Positive Number (Easy) (time: 2m 45):

```python3
class Solution:

    def findKthPositive(self, arr: List[int], k: int) -> int:
        (left, right) = (0, len(arr) - 1)
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k
```

## notes: 

After much struggle, finally solved this from memory.

---------------------

# 2025-10-26 15:32: 821. Shortest Distance to a Character (Easy) (time: 7m 32):

```python3
from typing import List
'\nURL: https://leetcode.com/problems/shortest-distance-to-a-character/description/?envType=problem-list-v2&envId=vn57k9wr\n\n821. Shortest Distance to a Character\n\nGiven a string s and a character c that occurs in s, return an array of integers answer where answer.length == s.length and answer[i] is the distance from index i to the closest occurrence of character c in s.\n\nThe distance between two indices i and j is abs(i - j), where abs is the absolute value function.\n\nExample 1:\n\nInput: s = "loveleetcode", c = "e"\nOutput: [3,2,1,0,1,0,0,1,2,2,1,0]\nExplanation: The character \'e\' appears at indices 3, 5, 6, and 11 (0-indexed).\nThe closest occurrence of \'e\' for index 0 is at index 3, so the distance is abs(0 - 3) = 3.\nThe closest occurrence of \'e\' for index 1 is at index 3, so the distance is abs(1 - 3) = 2.\nFor index 4, there is a tie between the \'e\' at index 3 and the \'e\' at index 5, but the distance is still the same: abs(4 - 3) == abs(4 - 5) = 1.\nThe closest occurrence of \'e\' for index 8 is at index 6, so the distance is abs(8 - 6) = 2.\n\nExample 2:\n\nInput: s = "aaab", c = "b"\nOutput: [3,2,1,0]\n\nConstraints:\n\n    1 <= s.length <= 10^4\n    s[i] and c are lowercase English letters.\n    It is guaranteed that c occurs at least once in s.\n'

class Solution:

    def shortestToChar(self, s: str, c: str) -> List[int]:
        last_pos_left = None
        last_pos_right = None
        res = []
        for i in range(len(s)):
            if s[i] == c:
                last_pos_left = i
            dist_from_left = i - last_pos_left if last_pos_left is not None else maxsize
            res.append(dist_from_left)
        for i in range(len(s) - 1, -1, -1):
            if s[i] == c:
                last_pos_right = i
            dist_from_right = last_pos_right - i if last_pos_right is not None else maxsize
            res[i] = min(res[i], dist_from_right)
        return res
```

---------------------

# 2025-10-27 04:24: 1837. Sum of Digits in Base K (Easy) (time: 13m 53):

```python3
class Solution:

    def toBase(self, n, k):
        res = []
        while n:
            (n, m) = divmod(n, k)
            res = [m] + res
        return reduce(lambda acc, val: acc * 10 + val, res)

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def sumBase(self, n: int, k: int) -> int:
        n = self.toBase(n, k)
        digits = self.getDigits(n)
        return sum(digits)
```

## notes: 

Base conversion is one of those things that easily slips my mind.

Let's go through some base conversions by hand:

10 in binary as base 10:

1           0
2^1 * 1     2^0 * 0


The above method involves working directly with the digits.

However we can also use divmod, e.g going from 10 base 10 to binary:

>>> divmod(10, 2)
(5, 0)
>>> divmod(5, 2)
(2, 1)
>>> divmod(2, 2)
(1, 0)
>>> divmod(1, 2)
(0, 1)

The output being 0101.

So we recursively run divmod on the number until we get 0, and the remainder
forms the digits of the new base.

---------------------

# 2025-10-27 04:59: 599. Minimum Index Sum of Two Lists (Easy) (time: 11m 29):

```python3
class Solution:

    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        D = {v: i for (i, v) in enumerate(list2)}
        common = defaultdict(list)
        for (i, r) in enumerate(list1):
            if r in D:
                common[i + D[r]].append(r)
        return common[min(common.keys())]
```

---------------------

# 2025-10-27 05:37: 2043. Simple Bank System (Medium) (time: 10m 31):

```python3
class Bank:

    def __init__(self, balance: List[int]):
        self.B = {i + 1: v for (i, v) in enumerate(balance)}

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if account1 in self.B and account2 in self.B and (self.B[account1] >= money):
            self.B[account1] -= money
            self.B[account2] += money
            return True
        return False

    def deposit(self, account: int, money: int) -> bool:
        if account in self.B:
            self.B[account] += money
            return True
        return False

    def withdraw(self, account: int, money: int) -> bool:
        if account in self.B and self.B[account] >= money:
            self.B[account] -= money
            return True
        return False
balance = [10, 100, 20, 50, 30]
```

---------------------

# 2025-10-27 06:23: 46. Permutations (Medium) - learning (time: 22m 31):

```python3
class Solution:

    def permute(self, nums: List[int]) -> List[List[int]]:

        def dfs(i):
            if i == len(nums):
                res.append(nums[:])
                return
            for j in range(i, len(nums)):
                (nums[i], nums[j]) = (nums[j], nums[i])
                dfs(i + 1)
                (nums[i], nums[j]) = (nums[j], nums[i])
        res = []
        dfs(0)
        return res
```

## notes: 

Hmm i'm only getting:

[[1, 2, 3], [2, 1, 3], [2, 3, 1]]

Duh.. i was close, but had to look up the solution.

The real insight i missed on was the for loop.

                           [1,2,3]   ← dfs(0)
                          /     |     \
                         /      |      \
                        /       |       \
                swap(0,0)  swap(0,1)  swap(0,2)
                   ↓          ↓          ↓
               [1,2,3]     [2,1,3]     [3,2,1]
                 |            |            |
              dfs(1)        dfs(1)       dfs(1)
              /   \         /   \         /   \
             /     \       /     \       /     \
      swap(1,1) swap(1,2) swap(1,1) swap(1,2) swap(1,1) swap(1,2)
         ↓         ↓         ↓         ↓         ↓         ↓
     [1,2,3]   [1,3,2]   [2,1,3]   [2,3,1]   [3,2,1]   [3,1,2]
        |         |         |         |         |         |
      dfs(2)    dfs(2)    dfs(2)    dfs(2)    dfs(2)    dfs(2)
        |         |         |         |         |         |
        ↓         ↓         ↓         ↓         ↓         ↓
     [1,2,3]   [1,3,2]   [2,1,3]   [2,3,1]   [3,2,1]   [3,1,2]
        |         |         |         |         |         |
     dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅

i is the starting index of each recursive branch (so i + 1 on the next recursion),
and we range from i to n as j.

Hard to mentally visualize.

---------------------

# 2025-10-27 07:14: 47. Permutations II (Medium) (time: 26m 48):

```python3
class Solution:

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:

        def dfs(i):
            if i == len(nums):
                res.add(tuple(nums[:]))
                return
            for j in range(i, len(nums)):
                if i != j and nums[i] == nums[j]:
                    continue
                (nums[i], nums[j]) = (nums[j], nums[i])
                dfs(i + 1)
                (nums[i], nums[j]) = (nums[j], nums[i])
        res = set()
        dfs(0)
        return list(map(list, res))
```

## notes: 

dfs(0)
                                                        |
                                    swap 0, 0        swap 0, 1      swap 0, 2
                                    [1, 1, 2]        [1, 1, 2]      [2, 1, 1]

                            dfs(1)                    dfs(1)                    dfs(1)

swap 1, 1     swap 1, 2
[1, 1, 2]     [1, 2, 1]


swap 2, 2     swap 2, 2
[1, 1, 2]     [1, 2, 1]

[1, 1, 2].    [1, 2, 1]

Hmm this feels like it's not the right solution, since i had to resort to using a set.

---------------------

# 2025-10-27 09:22: 47. Permutations II (Medium) (time: 2m 38):

```python3
class Solution:

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:

        def dfs(i):
            if i == len(nums):
                res.append(nums[:])
                return
            for j in range(i, len(nums)):
                if j > i and nums[j - 1] == nums[j]:
                    continue
                (nums[i], nums[j]) = (nums[j], nums[i])
                dfs(i + 1)
                (nums[i], nums[j]) = (nums[j], nums[i])
        nums.sort()
        res = []
        dfs(0)
        return res
```

## notes: 

Consulted Grok for a better way to deal with duplicates.

It seems sorting, and checking on the previous adjacent j does it, which seems obvious
with hindsight.

---------------------

# 2025-10-27 11:04: 410. Split Array Largest Sum (Hard) - learning (time: 94m 36):

```python3
class Solution:

    def count_smaller_subarrays(self, nums, max_sum, m):
        (cuts, prefix) = (0, 0)
        for x in nums:
            if x > max_sum:
                return False
            prefix += x
            if prefix > max_sum:
                cuts += 1
                prefix = x
        return cuts + 1

    def can_split(self, nums, max_sum, m):
        return self.count_smaller_subarrays(nums, max_sum, m) <= m

    def splitArray(self, nums: List[int], k: int) -> int:
        low = max(nums)
        high = sum(nums)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if self.can_split(nums, mid, k):
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

OK i had to look at solutions, and consult Grok to piece this together. I like this solution a lot,
but will need to revisit this problem at a later date, and solve it myself.

---------------------

# 2025-10-27 11:50: 1652. Defuse the Bomb (Easy) (time: 21m 26):

```python3
class Solution:

    def decrypt(self, code: List[int], k: int) -> List[int]:
        res = [0] * len(code)
        for i in range(len(code)):
            if k > 0:
                for j in range(i + 1, i + k + 1):
                    res[i] += code[j % len(code)]
            elif k < 0:
                for j in range(i - 1, i + k - 1, -1):
                    res[i] += code[j % len(code)]
        return res
```

## notes: 

Those negative indices were tricky.

---------------------

# 2025-10-27 12:14: 897. Increasing Order Search Tree (Easy) (time: 4m 55):

```python3
class Solution:

    def increasingBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            nodes.append(node)
            dfs(node.right)
        nodes = []
        dfs(root)
        for i in range(len(nodes)):
            nodes[i].left = None
            nodes[i].right = nodes[i + 1] if i + 1 < len(nodes) else None
        return nodes[0]
```

---------------------

# 2025-10-27 12:23: 3184. Count Pairs That Form a Complete Day I (Easy) (time: 4m 27):

```python3
class Solution:

    def countCompleteDayPairs(self, hours: List[int]) -> int:
        return sum((i < j and (hours[i] + hours[j]) % 24 == 0 for (i, j) in combinations(range(len(hours)), 2)))
```

---------------------

# 2025-10-27 13:57: 589. N-ary Tree Preorder Traversal (Easy) (time: 4m 43):

```python3
class Node:

    def __init__(self, val: Optional[int]=None, children: Optional[List['Node']]=None):
        self.val = val
        self.children = children if children is not None else []

def build_nary_tree(data: List[Optional[int]]) -> Optional[Node]:
    if not data or data[0] is None:
        return None
    root = Node(data[0])
    queue = deque([root])
    i = 2
    while queue and i < len(data):
        parent = queue.popleft()
        while i < len(data) and data[i] is not None:
            child = Node(data[i])
            parent.children.append(child)
            queue.append(child)
            i += 1
        i += 1
    return root

class Solution:

    def preorder(self, root: 'Node') -> List[int]:

        def dfs(node):
            if not node:
                return
            res.append(node.val)
            for c in node.children:
                dfs(c)
        res = []
        dfs(root)
        return res
```

---------------------

# 2025-10-27 15:52: 2226. Maximum Candies Allocated to K Children (Medium) (time: 20m 38):

```python3
class Solution:

    def tryPiles(self, candies, size):
        return sum((x // size for x in candies))

    def maximumCandies(self, candies: List[int], k: int) -> int:
        low = 1
        high = max(candies)
        result = 0
        is_minimization = False
        while low <= high:
            mid = low + (high - low) // 2
            num_kids = self.tryPiles(candies, mid)
            if num_kids >= k:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

Took longer than it should. Post lunch brain fog.

---------------------

# 2025-10-28 12:12: 1870. Minimum Speed to Arrive on Time (Medium) - learning (time: 24m 54):

```python3
class Solution:

    def travelTime(self, dist, speed):
        ceil = lambda a, b: (a + b - 1) // b
        return sum((ceil(d, speed) if i < len(dist) - 1 else d / speed for (i, d) in enumerate(dist)))

    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1
        high = max(10 ** 7, int(dist[-1] / (hour - (n - 1))) + 1)
        low = 1
        result = -1
        while low <= high:
            speed = low + (high - low) // 2
            if self.travelTime(dist, speed) <= hour:
                result = speed
                high = speed - 1
            else:
                low = speed + 1
        return result
```

## notes: 

This question is beating the life out of me. I want to read the solution.
This is not my solution.

I was able to come up with the travelTime check, for example, computing
`high` was above and beyond me.

---------------------

# 2025-10-28 14:18: 1760. Minimum Limit of Balls in a Bag (Medium) - learning (time: 40m 10):

```python3
class Solution:

    def check_condition(self, nums, penalty, max_operations):
        ceil_div = lambda a, b: (a + b - 1) // b
        total_ops = 0
        for x in nums:
            total_ops += ceil_div(x, penalty) - 1
            if total_ops > max_operations:
                return False
        return total_ops <= max_operations

    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        low = 1
        high = max(nums)
        result = -1
        while low <= high:
            mid = low + (high - low) // 2
            if self.check_condition(nums, mid, maxOperations):
                result = mid
                high = mid - 1
            else:
                low = mid + 1
        return result
```

## notes: 

[7, 17], 3 ->

3, 4, 17
3, 4, 11, 6
3, 4, 5, 6, 6

Hint 1:

> Let's change the question if we know the maximum size of a bag what is the minimum number of bags you can make

Ok so we need to flip our thinking here. We guess the maximum size of a bag is 6.. so how do we compute
the minimum number of bags we can make?

Guess = 5
Operations = 3
Bags = [7, 17]

I could try to get 6 from 17, i.e 11 and 6. then same with 11.

So take the max, and subtract 6 to get [7, 11, 6], then do the same with 11..
11-6 = 5, so [7, 5, 6, 6] but surely
it's not that simple to just subtract the guess each time.

Let's try some different numbers:

Guess = 3
Operations = 4
Bags = [5, 5, 5]

We take the max, 5. subtract 3, which leaves us with 3, 2
Do that 3 times to get:

[3,3,3,2,2,2]

On our 4th operation, we can do [3,3,3,0,2,2,2]

Ok let's look at bigger examples now:


Guess = 500000000
Operations = 1
Bags = [1000000000]

We take the max, and subtract 500000000, to get [500000000,500000000]
Ok that works too.

I'll check the second hint to make sure.

> note that as the maximum size increases the minimum number of bags decreases so we can binary search the maximum size

Hmm i have no idea what this means. I think this just means there's an inverse relationship between the max bag and min
number of bags, so it's encouraging us to do a bs.

Hmm i give up because i've overtime. I think i was very close.. but in check_condition, it's not a matter
of subtracting the penalty from the max.

Not my solution.

---------------------

# 2025-10-28 14:30: Review Notes

Ok so today i ran into some issues because i'm fuzzy when it comes to ceiling division, so broadly speaking a math thing.

# 1870. Minimum Speed to Arrive on Time

I used ceil(dist / speed) which i'm being told is incorrect, i should be using:

ceil_div = lambda a, b: (a + b - 1) // b

to avoid floating point errors.

Also in the solution:

```python
class Solution:

    def travelTime(self, dist, speed):
        ceil = lambda a, b: (a + b - 1) // b
        return sum(
            ceil(d, speed) if i < len(dist) - 1 else d / speed
            for i, d in enumerate(dist)
        )

    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1
        high = max(10**7, int(dist[-1] / (hour - (n - 1))) + 1)
        low = 1
        result = -1
        while low <= high:
            speed = low + (high - low) // 2
            if self.travelTime(dist, speed) <= hour:
                result = speed
                high = speed - 1
            else:
                low = speed + 1
        return result
```

I'm massively confused by:

```python
if hour <= n - 1:
    return -1
```

As well as:

```python
high = max(10**7, int(dist[-1] / (hour - (n - 1))) + 1)
```

Computing this or gaining an intuition for it is hard, making me think i need to work on more (simpler) array or math problems involving ceiled divisions.

# 1760. Minimum Limit of Balls in a Bag

Same here.. my solution was close.. but inefficient and potentially wrong:

```python
    def check_condition(self, nums, penalty, operations):
        nums = [-x for x in nums]
        for _ in range(operations):
            _max = -heappop(nums)
            if _max == penalty:
                return True
            rem = _max - penalty
            heappush(nums, -rem)
            heappush(nums, -penalty)
        return -heappop(nums) == penalty
```

The correct solution once again needs ceiled division.

```python
class Solution:
    def check_condition(self, nums, penalty, max_operations):
        ceil_div = lambda a, b: (a + b - 1) // b
        total_ops = 0
        for x in nums:
            total_ops += ceil_div(x, penalty) - 1
            if total_ops > max_operations:
                return False
        return total_ops <= max_operations

    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        low = 1
        high = max(nums)
        result = -1
        while low <= high:
            mid = low + (high - low) // 2
            if self.check_condition(nums, mid, maxOperations):
                result = mid
                high = mid - 1
            else:
                low = mid + 1
        return result
```

So at this point i think it would be wise to be recommended more problems relating to ceiled division, until i get comfortable with them.

---

I asked Grok for simpler problems involving ceiled division. Here's what it generated:

Here are some recommendations for problems that involve ceiling division (often implemented as `(a + b - 1) // b` in integer arithmetic). This technique is commonly used in optimization problems with binary search, which tend to be rated "Medium" on LeetCode—there aren't many (if any) "Easy" problems that feature it prominently in the optimal solution. The ones below are similar in concept to the one you shared (LeetCode 1760), but they might feel simpler depending on the context, as they apply the same idea in slightly different scenarios.

I'll include the problem number, title, a brief explanation of how ceiling division is used, and a link. All are Medium difficulty.

### 1. LeetCode 875: Koko Eating Bananas

- **How it uses ceiling division**: Binary search to minimize the eating speed `k`. The check function computes the total hours needed as `sum((pile + k - 1) // k for pile in piles)` and verifies if it's <= the allowed hours.
- **Why simpler?**: The scenario (eating bananas) is straightforward, and it's a classic intro to this pattern without additional twists.
- Link: https://leetcode.com/problems/koko-eating-bananas/

### 2. LeetCode 1283: Find the Smallest Divisor Given a Threshold

- **How it uses ceiling division**: Binary search to find the smallest divisor `d`. The check function calculates `sum((num + d - 1) // d for num in nums)` and checks if it's <= the threshold.
- **Why simpler?**: Very close to your problem's structure, but with a direct sum of ceils instead of subtracting 1 per bag.
- Link: https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/

### 3. LeetCode 1870: Minimum Speed to Arrive on Time

- **How it uses ceiling division**: Binary search to minimize the speed `s`. The check function computes the total time as `sum((dist[i] + s - 1) // s for i in range(len(dist)-1)) + dist[-1] / s` and verifies if it's <= the hour limit.
- **Why simpler?**: The floating-point handling for the last element adds a small variation, but the core ceil usage is clear and isolated.
- Link: https://leetcode.com/problems/minimum-speed-to-arrive-on-time/

### 4. LeetCode 2064: Minimized Maximum of Products Distributed to Any Store

- **How it uses ceiling division**: Binary search to minimize the max products per store. The check function counts stores needed as `sum((q + mid - 1) // mid for q in quantities)` and checks if it's <= `n`.
- **Why simpler?**: Similar to distributing balls/bananas, but focused on stores/products—easy to grasp if you've done the bag problem.
- Link: https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/

If you're looking for even simpler non-LeetCode examples to build intuition, consider basic math puzzles like:

- "How many groups of size `b` are needed to cover `a` items?" (Answer: `(a + b - 1) // b`.)
- Or practice implementing ceiling division without built-in functions, as in GeeksforGeeks articles on the topic.

If these aren't what you had in mind or you want recommendations from other platforms (e.g., Codeforces, HackerRank), let me know for more tailored suggestions!

---------------------

# 2025-10-28 14:52: 3712. Sum of Elements With Frequency Divisible by K (Easy) (time: 2m 24):

```python3
class Solution:

    def sumDivisibleByK(self, nums: List[int], k: int) -> int:
        counts = Counter(nums)
        return sum((item * count for (item, count) in counts.items() if count % k == 0))
```

---------------------

# 2025-10-28 15:08: 1304. Find N Unique Integers Sum up to Zero (Easy) (time: 6m 54):

```python3
class Solution:

    def sumZero(self, n: int) -> List[int]:
        res = []
        if n % 2 != 0:
            res.append(0)
        for i in range(1, n // 2 + 1):
            res.extend([i, -i])
        return res
```

---------------------

# 2025-10-28 15:25: 3461. Check If Digits Are Equal in String After Operations I (Easy) (time: 3m 47):

```python3
class Solution:

    def hasSameDigits(self, s: str) -> bool:
        nums = [int(x) for x in s]
        while len(nums) > 2:
            new = []
            for (a, b) in pairwise(nums):
                new.append((a + b) % 10)
            nums = new
        return nums[0] == nums[1]
```

---------------------

# 2025-10-28 15:48: 1812. Determine Color of a Chessboard Square (Easy) (time: 13m 59):

```python3
class Solution:

    def squareIsWhite(self, coordinates: str) -> bool:
        (col, row) = coordinates
        col = (ord(col) - ord('a')) % 2 != 0
        row = (int(row) - 1) % 2 != 0
        return col ^ row
```

---------------------

# 2025-10-28 15:51: 46. Permutations (Medium) (time: 2m 17):

```python3
class Solution:

    def permute(self, nums: List[int]) -> List[List[int]]:

        def dfs(i):
            if i == len(nums):
                res.append(nums[:])
            for j in range(i, len(nums)):
                (nums[i], nums[j]) = (nums[j], nums[i])
                dfs(i + 1)
                (nums[i], nums[j]) = (nums[j], nums[i])
        res = []
        dfs(0)
        return res
```

---------------------

# 2025-10-28 16:58: 3270. Find the Key of the Numbers (Easy) (time: 15m 14):

```python3
class Solution:

    def generateKey(self, num1: int, num2: int, num3: int) -> int:
        res = 0
        rem = lambda x: x % 10 if num1 else maxsize
        nums = []
        while num1 or num2 or num3:
            m = min([rem(num1), rem(num2), rem(num3)])
            nums.append(m if m != maxsize else 0)
            num1 //= 10
            num2 //= 10
            num3 //= 10
        for n in reversed(nums):
            res = res * 10 + n
        return res
```

---------------------

# 2025-10-28 17:13: 2578. Split With Minimum Sum (Easy) (time: 3m 31):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def splitNum(self, num: int) -> int:
        digits = self.getDigits(num)
        digits.sort()
        (a, b) = (0, 0)
        for (i, d) in enumerate(digits):
            if i % 2 == 0:
                a = a * 10 + d
            else:
                b = b * 10 + d
        return a + b
```

---------------------

# 2025-10-29 10:02: 2566. Maximum Difference by Remapping a Digit (Easy) (time: 21m 3):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits[::-1]

    def digitsToNum(self, digits):
        res = 0
        for d in digits:
            res = res * 10 + d
        return res

    def findFirstNonZero(self, digits):
        for (i, d) in enumerate(digits):
            if d != 0:
                return d

    def findFirstNonNine(self, digits):
        for (i, d) in enumerate(digits):
            if d != 9:
                return d

    def minMaxDifference(self, num: int) -> int:
        digits = self.getDigits(num)
        max_digit = digits[:]
        min_digit = digits[:]
        _min = self.findFirstNonNine(digits)
        _max = self.findFirstNonZero(digits)
        for (i, d) in enumerate(digits):
            if d == _min:
                max_digit[i] = 9
        for (i, d) in enumerate(digits):
            if d == _max:
                min_digit[i] = 0
        return self.digitsToNum(max_digit) - self.digitsToNum(min_digit)
```

## notes: 

For the maximum digit, get the right most digit that is not a 9.

---------------------

# 2025-10-29 10:37: 2651. Calculate Delayed Arrival Time (Easy) (time: 1m 48):

```python3
class Solution:

    def findDelayedArrivalTime(self, arrivalTime: int, delayedTime: int) -> int:
        return (arrivalTime + delayedTime) % 24
```

---------------------

# 2025-10-29 10:53: 2928. Distribute Candies Among Children I (Easy) (time: 11m 38):

```python3
class Solution:

    def distributeCandies(self, n: int, limit: int) -> int:
        res = []
        for i in range(limit + 1):
            for j in range(limit + 1):
                for k in range(limit + 1):
                    if sum([i, j, k]) == n:
                        res.append([i, j, k])
        return len(res)
```

---------------------

# 2025-10-29 11:02: 2169. Count Operations to Obtain Zero (Easy) (time: 2m 28):

```python3
class Solution:

    def countOperations(self, num1: int, num2: int) -> int:
        n = 0
        while num1 and num2:
            n += 1
            if num1 >= num2:
                num1 -= num2
            else:
                num2 -= num1
        return n
```

---------------------

# 2025-10-29 11:10: 3492. Maximum Containers on a Ship (Easy) (time: 5m 40):

```python3
class Solution:

    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return int(min(n * n, maxWeight / w))
```

## notes: 

They gave the answer in the 'hints' but this is a good example of a question i would have stumbled upon; that would have taken me a while, because maths.

---------------------

# 2025-10-29 11:12: Review Notes

# 3492. Maximum Containers on a Ship

This is a good example of a question i would have struggled to solved if it were not for the hints. So if a medium or hard question is maths heavy, for sure i'll stumble.

```
class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return int(min(n * n, maxWeight / w))
```

---

I asked grok to generate some questions involving ceiled div, and solved them.

```python
class Solution:
    def minDays(self, n: int, k: int) -> int:
        ceil_div = lambda a, b: (a + b - 1) // b
        return ceil_div(n, k)
```

and

```python
class Solution:
    def minCost(self, n: int, k: int, p: int) -> int:
        ceil_div = lambda a, b: (a + b - 1) // b
        return ceil_div(n, k) * p
```

They were easy.

---------------------

# 2025-10-29 11:22: 412. Fizz Buzz (Easy) (time: 2m 29):

```python3
class Solution:

    def fizzBuzz(self, n: int) -> List[str]:
        res = []
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                res.append('FizzBuzz')
            elif i % 3 == 0:
                res.append('Fizz')
            elif i % 5 == 0:
                res.append('Buzz')
            else:
                res.append(str(i))
        return res
```

---------------------

# 2025-10-29 11:36: 883. Projection Area of 3D Shapes (Easy) (time: 9m 55):

```python3
class Solution:

    def projectionArea(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        if not grid[0]:
            return 0
        col = lambda i: [grid[x][i] for x in range(len(grid))]
        z = sum((x != 0 for x in chain(*grid)))
        y = sum((max(row) for row in grid))
        x = sum((max(col(c)) for c in range(len(next(iter(grid), [])))))
        return x + y + z
```

---------------------

# 2025-10-29 13:51: 2187. Minimum Time to Complete Trips (Medium) (time: 12m 45):

```python3
class Solution:

    def numTripsCompleted(self, time, totaltime):
        return sum((totaltime // t for t in time))

    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        low = 1
        high = min(time) * totalTrips
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if self.numTripsCompleted(time, mid) >= totalTrips:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

## notes: 

Felt quite easy now, but maybe i got lucky.

---------------------

# 2025-10-29 15:35: 2064. Minimized Maximum of Products Distributed to Any Store (Medium) (time: 22m 29):

```python3
class Solution:

    def distribute(self, n, quantities, r):
        ceil_div = lambda a, b: (a + b - 1) // b
        return sum((ceil_div(q, r) for q in quantities))

    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        low = 1
        high = sum(quantities)
        result = -1
        is_minimization = True
        while low <= high:
            mid = low + (high - low) // 2
            if self.distribute(n, quantities, mid) <= n:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            elif is_minimization:
                low = mid + 1
            else:
                high = mid - 1
        return result
```

---------------------

# 2025-10-30 09:26: 3726. Remove Zeros in Decimal Representation (Easy) (time: 6m 25):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def removeZeros(self, n: int) -> int:
        res = 0
        digits = self.getDigits(n)
        for x in [x for x in digits[::-1] if x != 0]:
            res = res * 10 + x
        return res
```

---------------------

# 2025-10-30 09:40: 1742. Maximum Number of Balls in a Box (Easy) (time: 6m 33):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        boxes = defaultdict(int)
        for ball in range(lowLimit, highLimit + 1):
            numBalls = sum(self.getDigits(ball))
            boxes[numBalls] += 1
        return max(boxes.values())
```

---------------------

# 2025-10-30 09:56: 3079. Find the Sum of Encrypted Integers (Easy) (time: 5m 40):

```python3
class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def encrypt(self, digits):
        _max = max(digits)
        digits = [_max] * len(digits)
        res = 0
        for d in digits:
            res = res * 10 + d
        return res

    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res += self.encrypt(self.getDigits(n))
        return res
```

---------------------

# 2025-10-30 10:09: 3432. Count Partitions with Even Sum Difference (Easy) (time: 8m 37):

```python3
class Solution:

    def countPartitions(self, nums: List[int]) -> int:
        right_partition = sum(nums)
        left_partition = 0
        res = 0
        for i in range(len(nums)):
            left_partition += nums[i]
            right_partition -= nums[i]
            if i != 0 and (right_partition - left_partition) % 2 == 0:
                res += 1
        return res
```

---------------------

# 2025-10-30 11:11: 1030. Matrix Cells in Distance Order (Easy) (time: 23m 20):

```python3
class Solution:

    def allCellsDistOrder(self, rows: int, cols: int, rCenter: int, cCenter: int) -> List[List[int]]:
        res = []
        for row in range(rows):
            for col in range(cols):
                res.append([row, col])
        res.sort(key=lambda x: abs(x[0] - rCenter) + abs(x[1] - cCenter))
        return res
```

## notes: 

Terribly written question.

---------------------

# 2025-10-30 15:17: 1870. Minimum Speed to Arrive on Time (Medium) (time: 24m 20):

```python3
class Solution:

    def travelTime(self, dist, speed):
        ceil_div = lambda a, b: (a + b - 1) // b
        time = 0
        for (i, d) in enumerate(dist):
            if i < len(dist) - 1:
                time += ceil_div(d, speed)
            else:
                time += d / speed
        return time

    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        low = 1
        result = -1
        high = 10 ** 7
        while low <= high:
            speed = (low + high) // 2
            travelTime = self.travelTime(dist, speed)
            if travelTime <= hour:
                result = speed
                high = speed - 1
            else:
                low = speed + 1
        return result
```

## notes: 

The precision constraints in this problem made me feel sad.

Input: dist = [1,3,2], hour = 2.7

This wasn't 2.7... and rounding lead to everything else breaking.

Anyway.

---------------------

# 2025-10-30 16:52: 1760. Minimum Limit of Balls in a Bag (Medium) (time: 26m 27):

```python3
class Solution:

    def check_condition(self, nums, penalty):
        res = 0
        for n in nums:
            if n > penalty:
                res += ceil_div(n, penalty) - 1
        return res

    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        low = 1
        high = max(nums)
        res = -1
        if maxOperations == 0:
            return high
        while low <= high:
            mid = (low + high) // 2
            ops = self.check_condition(nums, mid)
            if ops <= maxOperations:
                res = mid
                high = mid - 1
            else:
                low = mid + 1
        return res
```

---------------------

# 2025-10-30 17:29: 410. Split Array Largest Sum (Hard) - learning (time: 20m 51):

```python3
class Solution:

    def count_smaller_subarrays(self, nums, max_sum):
        res = 0
        prefix = 0
        for n in nums:
            prefix += n
            if prefix >= max_sum:
                res += 1
                prefix = 0
        return res

    def can_split(self, nums, max_sum, m):
        prefix = 0
        for n in sorted(nums, reverse=True):
            prefix += n
            smaller_subs = self.count_smaller_subarrays(nums)

    def splitArray(self, nums: List[int], k: int) -> int:
        low = 1
        high = sum(nums)
        res = -1
        while low <= high:
            max_sum = (low + high) // 2
            can_split = self.can_split(nums, max_sum, k)
            if can_split:
                res = max_sum
                low = max_sum + 1
            else:
                high = max_sum - 1
        return res
```

## notes: 

I give up.

---------------------

# 2025-10-31 06:26: 91. Decode Ways (Medium) - learning (time: 21m 10):

```python3
class Solution:

    def numDecodings(self, s: str) -> int:

        @cache
        def dfs(i):
            if i < 0:
                return 1
            ways = 0
            if '1' <= s[i] <= '9':
                ways += dfs(i - 1)
            if i >= 1 and '10' <= s[i - 1:i + 1] <= '26':
                ways += dfs(i - 2)
            return ways
        res = dfs(len(s) - 1)
        return res
```

## notes: 

Had to look up a solution. Still feels like magic.

---------------------

# 2025-10-31 07:48: 1974. Minimum Time to Type Word Using Special Typewriter (Easy) - learning (time: 22m 27):

```python3
class Solution:

    def minTimeToType(self, word: str) -> int:
        (cnt, prev) = (len(word), 'a')
        for cur in word:
            diff = abs(ord(cur) - ord(prev))
            cnt += min(diff, 26 - diff)
            prev = cur
        return cnt
```

## notes: 

Couldn'f figure this out.

---------------------

# 2025-10-31 08:13: 2913. Subarrays Distinct Element Sum of Squares I (Easy) - learning (time: 11m 18):

```python3
class Solution:

    def sumCounts(self, nums: List[int]) -> int:

        def powerset(i):
            if sub:
                res.append(sub[:])
            for j in range(i, len(nums)):
                sub.append(nums[j])
                powerset(j + 1)
                sub.pop()
        sub = []
        res = []
        powerset(0)
        return res
```

## notes: 

I know how to compute the powerset, but this is different. It's asking for
all subarrays of all sizes.....

no clue.

---------------------

# 2025-10-31 08:49: 1827. Minimum Operations to Make the Array Increasing (Easy) (time: 6m 25):

```python3
class Solution:

    def minOperations(self, nums: List[int]) -> int:
        res = 0
        for (i, n) in enumerate(nums):
            if i > 0:
                if n <= nums[i - 1]:
                    res += nums[i - 1] - n + 1
                    nums[i] = nums[i - 1] + 1
        return res
```

---------------------

# 2025-10-31 09:03: 3168. Minimum Number of Chairs in a Waiting Room (Easy) (time: 2m 56):

```python3
class Solution:

    def minimumChairs(self, s: str) -> int:
        chairs = 0
        max_needed = 0
        for e in s:
            if e == 'E':
                chairs += 1
            else:
                chairs -= 1
            max_needed = max(max_needed, chairs)
        return max_needed
```

---------------------

# 2025-10-31 10:41: 1374. Generate a String With Characters That Have Odd Counts (Easy) (time: 2m 33):

```python3
class Solution:

    def generateTheString(self, n: int) -> str:
        if n % 2 != 0:
            return 'p' * n
        else:
            return 'p' * (n - 1) + 'z'
```

---------------------

# 2025-10-31 10:58: 3258. Count Substrings That Satisfy K-Constraint I (Easy) (time: 7m 30):

```python3
class Solution:

    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        count = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                satisfies_k = lambda x: x.count('1') <= k or x.count('0') <= k
                sat = satisfies_k(s[i:j + 1])
                count += sat
        return count
```

---------------------



Here is my readiness estimates:

[
  {
    "run_date": "2025-10-02",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-03",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-02-15"
  },
  {
    "run_date": "2025-10-07",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-08",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-09",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-10",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-10",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-11",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-12",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-13",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-14",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-01-15"
  },
  {
    "run_date": "2025-10-15",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2026-02-15",
    "contest_topics_readiness": {
      "arrays": 0.9,
      "strings": 0.9,
      "hash_table": 0.8,
      "dynamic_programming": 0.4,
      "math": 0.7,
      "sorting": 0.8,
      "greedy": 0.6,
      "depth_first_search": 0.7,
      "binary_search": 0.8,
      "breadth_first_search": 0.6,
      "tree": 0.7,
      "matrix": 0.7,
      "two_pointers": 0.9,
      "bit_manipulation": 0.6,
      "stack": 0.7,
      "heap": 0.6,
      "graph": 0.5,
      "prefix_sum": 0.7,
      "simulation": 0.6,
      "counting": 0.7,
      "sliding_window": 0.7,
      "union_find": 0.3,
      "linked_list": 0.7,
      "monotonic_stack": 0.5,
      "recursion": 0.6,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.4,
      "queue": 0.6,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.5,
      "memoization": 0.4,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-16",
    "contest_readiness": "2025-11-30",
    "faang_interview": "2026-02-28",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.5,
      "math": 0.75,
      "sorting": 0.85,
      "greedy": 0.65,
      "depth_first_search": 0.75,
      "binary_search": 0.9,
      "breadth_first_search": 0.7,
      "tree": 0.8,
      "matrix": 0.75,
      "two_pointers": 0.95,
      "bit_manipulation": 0.7,
      "stack": 0.75,
      "heap": 0.7,
      "graph": 0.6,
      "prefix_sum": 0.75,
      "simulation": 0.65,
      "counting": 0.75,
      "sliding_window": 0.75,
      "union_find": 0.3,
      "linked_list": 0.85,
      "monotonic_stack": 0.5,
      "recursion": 0.65,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.4,
      "queue": 0.65,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.5,
      "memoization": 0.45,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-15",
    "run_date": "2025-10-17",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.55,
      "math": 0.75,
      "sorting": 0.85,
      "greedy": 0.65,
      "depth_first_search": 0.75,
      "binary_search": 0.95,
      "breadth_first_search": 0.7,
      "tree": 0.8,
      "matrix": 0.75,
      "two_pointers": 0.95,
      "bit_manipulation": 0.75,
      "stack": 0.75,
      "heap": 0.75,
      "graph": 0.6,
      "prefix_sum": 0.8,
      "simulation": 0.65,
      "counting": 0.75,
      "sliding_window": 0.75,
      "union_find": 0.3,
      "linked_list": 0.9,
      "monotonic_stack": 0.5,
      "recursion": 0.65,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.4,
      "queue": 0.65,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.6,
      "memoization": 0.45,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-18",
    "contest_readiness": "2025-11-30",
    "faang_interview": "2026-02-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.65,
      "math": 0.75,
      "sorting": 0.85,
      "greedy": 0.7,
      "depth_first_search": 0.8,
      "binary_search": 0.95,
      "breadth_first_search": 0.75,
      "tree": 0.85,
      "matrix": 0.8,
      "two_pointers": 0.95,
      "bit_manipulation": 0.75,
      "stack": 0.8,
      "heap": 0.85,
      "graph": 0.65,
      "prefix_sum": 0.85,
      "simulation": 0.7,
      "counting": 0.8,
      "sliding_window": 0.8,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.7,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.4,
      "queue": 0.7,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.7,
      "memoization": 0.5,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-19",
    "contest_readiness": "2026-01-15",
    "faang_interview": "2026-04-01",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.7,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.75,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.8,
      "stack": 0.85,
      "heap": 0.9,
      "graph": 0.7,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.75,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.75,
      "memoization": 0.55,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-20",
    "contest_readiness": "2025-11-20",
    "faang_interview": "2026-01-20",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.65,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.75,
      "depth_first_search": 0.85,
      "binary_search": 0.9,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.85,
      "stack": 0.85,
      "heap": 0.85,
      "graph": 0.7,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.75,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.8,
      "memoization": 0.55,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-21",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-01",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.7,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.75,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.85,
      "heap": 0.9,
      "graph": 0.7,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.75,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.85,
      "memoization": 0.55,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-22",
    "contest_readiness": "2025-11-22",
    "faang_interview": "2026-01-22",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.75,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.8,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.85,
      "heap": 0.9,
      "graph": 0.75,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.75,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.9,
      "memoization": 0.6,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-23",
    "contest_readiness": "2025-11-15",
    "faang_interview": "2025-12-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.8,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.8,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.85,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.8,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.9,
      "memoization": 0.6,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-25",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.7,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.8,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.85,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.8,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.8,
      "memoization": 0.6,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-26",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-01",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.85,
      "dynamic_programming": 0.75,
      "math": 0.8,
      "sorting": 0.85,
      "greedy": 0.8,
      "depth_first_search": 0.85,
      "binary_search": 0.95,
      "breadth_first_search": 0.8,
      "tree": 0.9,
      "matrix": 0.85,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.85,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.9,
      "simulation": 0.75,
      "counting": 0.85,
      "sliding_window": 0.85,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.8,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.75,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.8,
      "memoization": 0.6,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-27",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-02-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.9,
      "dynamic_programming": 0.8,
      "math": 0.85,
      "sorting": 0.9,
      "greedy": 0.85,
      "depth_first_search": 0.9,
      "binary_search": 0.95,
      "breadth_first_search": 0.85,
      "tree": 0.95,
      "matrix": 0.9,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.9,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.95,
      "simulation": 0.8,
      "counting": 0.9,
      "sliding_window": 0.9,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.85,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.8,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.85,
      "memoization": 0.65,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-28",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-01",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.9,
      "dynamic_programming": 0.7,
      "math": 0.85,
      "sorting": 0.9,
      "greedy": 0.85,
      "depth_first_search": 0.9,
      "binary_search": 0.9,
      "breadth_first_search": 0.85,
      "tree": 0.95,
      "matrix": 0.9,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.9,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.95,
      "simulation": 0.8,
      "counting": 0.9,
      "sliding_window": 0.9,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.85,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.8,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.8,
      "memoization": 0.65,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-29",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.9,
      "dynamic_programming": 0.75,
      "math": 0.85,
      "sorting": 0.9,
      "greedy": 0.85,
      "depth_first_search": 0.9,
      "binary_search": 0.95,
      "breadth_first_search": 0.85,
      "tree": 0.95,
      "matrix": 0.9,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.9,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.95,
      "simulation": 0.8,
      "counting": 0.9,
      "sliding_window": 0.9,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.85,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.8,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.85,
      "memoization": 0.7,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  },
  {
    "run_date": "2025-10-30",
    "contest_readiness": "2025-12-15",
    "faang_interview": "2026-03-15",
    "contest_topics_readiness": {
      "arrays": 0.95,
      "strings": 0.95,
      "hash_table": 0.9,
      "dynamic_programming": 0.8,
      "math": 0.9,
      "sorting": 0.9,
      "greedy": 0.85,
      "depth_first_search": 0.9,
      "binary_search": 1.0,
      "breadth_first_search": 0.85,
      "tree": 0.95,
      "matrix": 0.9,
      "two_pointers": 0.95,
      "bit_manipulation": 0.9,
      "stack": 0.9,
      "heap": 0.95,
      "graph": 0.8,
      "prefix_sum": 0.95,
      "simulation": 0.8,
      "counting": 0.9,
      "sliding_window": 0.9,
      "union_find": 0.3,
      "linked_list": 0.95,
      "monotonic_stack": 0.5,
      "recursion": 0.85,
      "trie": 0.4,
      "divide_and_conquer": 0.5,
      "bitmask": 0.45,
      "queue": 0.8,
      "topological_sort": 0.3,
      "segment_tree": 0.2,
      "game_theory": 0.2,
      "hash_function": 0.3,
      "binary_indexed_tree": 0.2,
      "string_matching": 0.5,
      "rolling_hash": 0.2,
      "shortest_path": 0.3,
      "number_theory": 0.4,
      "interactive": 0.1,
      "brainteaser": 0.5,
      "randomized": 0.2,
      "monotonic_queue": 0.4,
      "merge_sort": 0.5,
      "iterator": 0.3,
      "concurrency": 0.1,
      "probability_and_statistics": 0.2,
      "geometry": 0.3,
      "ordered_set": 0.3,
      "database": 0.2,
      "design": 0.4,
      "backtracking": 0.8,
      "memoization": 0.75,
      "quickselect": 0.3,
      "bucket_sort": 0.3,
      "minimum_spanning_tree": 0.2,
      "counting_sort": 0.4,
      "shell": 0.1,
      "line_sweep": 0.2,
      "reservoir_sampling": 0.1,
      "strongly_connected_component": 0.1,
      "eulerian_circuit": 0.1,
      "radix_sort": 0.2,
      "rejection_sampling": 0.1,
      "biconnected_component": 0.1
    }
  }
]


