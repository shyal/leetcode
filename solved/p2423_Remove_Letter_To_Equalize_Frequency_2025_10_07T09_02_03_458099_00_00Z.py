"""
URL: https://leetcode.com/problems/remove-letter-to-equalize-frequency/description/

2423. Remove Letter To Equalize Frequency

You are given a 0-indexed string word, consisting of lowercase English letters. You need to select one index and remove the letter at that index from word so that the frequency of every letter present in word is equal.

Return true if it is possible to remove one letter so that the frequency of all letters in word are equal, and false otherwise.

Note:

    The frequency of a letter x is the number of times it occurs in the string.
    You must remove exactly one letter and cannot choose to do nothing.


Example 1:

Input: word = "abac"
Output: true
Explanation: The letters that appear in word are 'a', 'b', 'a', 'c'. The frequencies of these letters are 2, 1, 2, 1. We can delete one occurrance of 'a', after which the letters in word become 'a', 'b', 'c', and their frequencies are 1, 1, 1. The frequencies of the letters are the same.

Example 2:

Input: word = "bcccc"
Output: true
Explanation: The letters that appear in word are 'b', 'c', 'c', 'c', 'c', and their frequencies are 1, 4. We can delete 'b', after which the letters in word become 'c', 'c', 'c', 'c', and their frequencies are 4. The frequencies of the letters are the same.

Example 3:

Input: word = "aazz"
Output: false
Explanation: The letters that appear in word are 'a', 'a', 'z', 'z', and their frequencies are 2, 2. No matter which letter we delete, the frequencies of 'a' and 'z' will be different.


Constraints:

    2 <= word.length <= 100
    word consists of only lowercase English letters.

---

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

"""


class Solution:
    def equalFrequency(self, word: str) -> bool:
        for i in range(len(word)):
            sub = word[:i] + word[i + 1 :]
            freq = list(dict(Counter(sub)).values())
            if len(set(freq)) == 1:
                return True
        return False


sol = Solution()

assert sol.equalFrequency("aazz") == False
assert sol.equalFrequency("abc") == True
assert sol.equalFrequency("aaabbbccc") == False
assert sol.equalFrequency("aabb") == False
assert sol.equalFrequency("bcccc") == True
assert sol.equalFrequency("cccd") == True
assert sol.equalFrequency("aa") == True
assert sol.equalFrequency("aaa") == True
assert sol.equalFrequency("abac") == True
assert sol.equalFrequency("abcc") == True
assert sol.equalFrequency("abccc") == False
assert sol.equalFrequency("ddaccb") == False
assert sol.equalFrequency("abacaba") == False
