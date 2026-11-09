# Given a string document, return a list of [word, count] pairs, one per
# distinct word, with the count as a string. Order the pairs by count,
# largest first; pairs with the same count keep the order in which their
# word first appears in document. A word is a run of characters between
# whitespace with every non-letter character removed and every letter
# lowercased. A run with no letters is not a word.
#
# Example 1:
#
# Input: document = "Practice makes perfect. you'll only get Perfect by practice. just practice!"
# Output: [["practice", "3"], ["perfect", "2"], ["makes", "1"], ["youll", "1"], ["only", "1"], ["get", "1"], ["by", "1"], ["just", "1"]]
# Explanation: "Perfect" and "perfect." are the same word. "you'll" loses
# its apostrophe. The six words with count 1 are in order of first
# appearance.
#
# Example 2:
#
# Input: document = "To be, or not to be, that is the question:"
# Output: [["to", "2"], ["be", "2"], ["or", "1"], ["not", "1"], ["that", "1"], ["is", "1"], ["the", "1"], ["question", "1"]]
#
# Example 3:
#
# Input: document = ""
# Output: []
#
# Constraints:
#
#     0 <= len(document) <= 10^5
#     document holds letters, digits, punctuation and whitespace.
#
#     REQUIRED: O(n) time for n = len(document). NO sorted(), NO
#     list.sort(), NO heap.
#
# ---

# mu 0.16

from string import ascii_lowercase

class Solution
  def word_count_engine(document: str) -> [[str]]
    if not document
      return []
    asc = set(ascii_lowercase + ' ')
    d = [x for x in d if x] = d.split(' ') = ''.join(x for x in d if x in asc) = d.lower() = document
    appearance = {:int}
    for >i, w in d
      if w not in appearance
        appearance[w] = i
    cnt = Counter(d)
    [[k, str(v)] for k, v in sorted(cnt.items(), key= x -> [x[1], -appearance[x[0]]], reverse=true)]
    


sol = Solution()

print(sol.word_count_engine("Practice makes perfect. you'll only get Perfect by practice. just practice!"))

# [['practice', '3'], ['perfect', '2'], ['makes', '1'], ['youll', '1'], ['only', '1'], ['get', '1'], ['by', '1'], ['just', '1']]

assert sol.word_count_engine("Practice makes perfect. you'll only get Perfect by practice. just practice!") == [['practice', '3'], ['perfect', '2'], ['makes', '1'], ['youll', '1'], ['only', '1'], ['get', '1'], ['by', '1'], ['just', '1']]
assert sol.word_count_engine('To be, or not to be, that is the question:') == [['to', '2'], ['be', '2'], ['or', '1'], ['not', '1'], ['that', '1'], ['is', '1'], ['the', '1'], ['question', '1']]
assert sol.word_count_engine('') == []
assert sol.word_count_engine("Practice makes perfect, you'll get perfecT by practice. just practice! just just just!!") == [['just', '4'], ['practice', '3'], ['perfect', '2'], ['makes', '1'], ['youll', '1'], ['get', '1'], ['by', '1']]
assert sol.word_count_engine('Every book is a quotation; and every      house is a quotation out of all forests, and mines,  and stone quarries; and every man is a quotation from all his ancestors. ') == [['and', '4'], ['every', '3'], ['is', '3'], ['a', '3'], ['quotation', '3'], ['all', '2'], ['book', '1'], ['house', '1'], ['out', '1'], ['of', '1'], ['forests', '1'], ['mines', '1'], ['stone', '1'], ['quarries', '1'], ['man', '1'], ['from', '1'], ['his', '1'], ['ancestors', '1']]
assert sol.word_count_engine('I have failed over and over and over again in my life and that is why I succeed.') == [['over', '3'], ['and', '3'], ['i', '2'], ['have', '1'], ['failed', '1'], ['again', '1'], ['in', '1'], ['my', '1'], ['life', '1'], ['that', '1'], ['is', '1'], ['why', '1'], ['succeed', '1']]
assert sol.word_count_engine('Look If you had One shot, Or one opportunity, To seize everything you ever wanted, In one moment, Would you capture it, Or just let it slip?') == [['you', '3'], ['one', '3'], ['or', '2'], ['it', '2'], ['look', '1'], ['if', '1'], ['had', '1'], ['shot', '1'], ['opportunity', '1'], ['to', '1'], ['seize', '1'], ['everything', '1'], ['ever', '1'], ['wanted', '1'], ['in', '1'], ['moment', '1'], ['would', '1'], ['capture', '1'], ['just', '1'], ['let', '1'], ['slip', '1']]
assert sol.word_count_engine("Cause I'm Slim Shady, yes I'm the real Shady, All you other Slim Shadys are just imitating So won't the real Slim Shady, please stand up, Please stand up, Please stand up") == [['slim', '3'], ['shady', '3'], ['please', '3'], ['stand', '3'], ['up', '3'], ['im', '2'], ['the', '2'], ['real', '2'], ['cause', '1'], ['yes', '1'], ['all', '1'], ['you', '1'], ['other', '1'], ['shadys', '1'], ['are', '1'], ['just', '1'], ['imitating', '1'], ['so', '1'], ['wont', '1']]
assert sol.word_count_engine('   ') == []
assert sol.word_count_engine('123 !!! 4-5') == []
assert sol.word_count_engine('a') == [['a', '1']]
assert sol.word_count_engine('A a A') == [['a', '3']]
assert sol.word_count_engine('b a b a') == [['b', '2'], ['a', '2']]
assert sol.word_count_engine('a b c b c c') == [['c', '3'], ['b', '2'], ['a', '1']]
assert sol.word_count_engine('x1y2z x-y-z xyz') == [['xyz', '3']]
assert sol.word_count_engine(' '.join(['w'] * 50000)) == [['w', '50000']]
names = [''.join((chr(97 + i // 26 ** k % 26) for k in 0..<3)) for i in 0..<17576]
assert sol.word_count_engine(' '.join(names)) == [[w, '1'] for w in names]
