"""
URL: https://leetcode.com/problems/find-duplicate-file-in-system/description/?envType=problem-list-v2&envId=vn57k9wr

609. Find Duplicate File in System

Given a list paths of directory info, including the directory path, and all the files with contents in this directory, return all the duplicate files in the file system in terms of their paths. You may return the answer in any order.

A group of duplicate files consists of at least two files that have the same content.

A single directory info string in the input list has the following format:

"root/d1/d2/.../dm f1.txt(f1_content) f2.txt(f2_content) ... fn.txt(fn_content)"

It means there are n files (f1.txt, f2.txt ... fn.txt) with content (f1_content, f2_content ... fn_content) respectively in the directory "root/d1/d2/.../dm". Note that n >= 1 and m >= 0. If m = 0, it means the directory is just the root directory.

The output is a list of groups of duplicate file paths. For each group, it contains all the file paths of the files that have the same content. A file path is a string that has the following format:

"directory_path/file_name.txt"

Example 1:

Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]

Example 2:

Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)"]
Output: [["root/a/2.txt","root/c/d/4.txt"],["root/a/1.txt","root/c/3.txt"]]

Constraints:

    1 <= paths.length <= 2 * 10^4
    1 <= paths[i].length <= 3000
    1 <= sum(paths[i].length) <= 5 * 10^5
    paths[i] consist of English letters, digits, '/', '.', '(', ')', and ' '.
    You may assume no files or directories share the same name in the same directory.
    You may assume each given directory info represents a unique directory. A single blank space separates the directory path and file info.
---
the input format is the paths:
["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]

root/a 1.txt(abcd)
root/a 2.txt(efgh)
root/c 3.txt(abcd)
root/c/d 4.txt(efgh)
root/c/d 4.txt(efgh)
root 4.txt(efgh)

the output is:
[["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]

seems to be grouped by content

efgh:

root/a/2.txt
root/c/d/4.txt
root/4.txt

root/a/1.txt
root/c/3.txt

so there is some expansion, and deduping work required, as well as classifying by content

expansion means turning this: root/a 1.txt(abcd) 2.txt(efgh)
into
abcd: root/a/1.txt
efgh: root/a/2.txt

LEETCODE: Accepted (17 ms, 26.4 MB)
"""


# mu 0.7
# def findDuplicate(paths: [str]) -> [[str]]
#   by_content = {:list}
#   for p in paths
#     c = p.split ' '
#     path, files = c[0], c[1:]
#     for file in files
#       filename, content = file.split('(')
#       content = content.split(')')[0]
#       by_content[content] <- path + '/' + filename
#   [v for v in by_content.values() if len(v) > 1]

from collections import defaultdict


class Solution:
    def findDuplicate(self, paths: list[str]) -> list[list[str]]:
        by_content = defaultdict(list)
        for p in paths:
            c = p.split(' ')
            path, files = c[0], c[1:]
            for file in files:
                filename, content = file.split('(')
                content = content.split(')')[0]
                by_content[content].append(path + '/' + filename)
        return [v for v in by_content.values() if len(v) > 1]


sol = Solution()
paths1 = ['root/a 1.txt(abcd) 2.txt(efgh)', 'root/c 3.txt(abcd)', 'root/c/d 4.txt(efgh)', 'root 4.txt(efgh)']
print(sol.findDuplicate(paths1))
expected1 = [['root/a/2.txt', 'root/c/d/4.txt', 'root/4.txt'], ['root/a/1.txt', 'root/c/3.txt']]
res1 = sol.findDuplicate(paths1)
_l, _r = set(map(frozenset, res1)), set(map(frozenset, expected1))
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
paths2 = ['root/a 1.txt(abcd) 2.txt(efgh)', 'root/c 3.txt(abcd)', 'root/c/d 4.txt(efgh)']
res2 = sol.findDuplicate(paths2)
expected2 = [['root/a/2.txt', 'root/c/d/4.txt'], ['root/a/1.txt', 'root/c/3.txt']]
_l, _r = set(map(frozenset, res2)), set(map(frozenset, expected2))
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = set(map(frozenset, sol.findDuplicate(['root 1.txt(a)']))), set()
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
