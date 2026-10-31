# URL: https://leetcode.com/problems/longest-string-chain/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1048. Longest String Chain
#
# You are given an array of words where each word consists of lowercase English letters.
#
# word_A is a predecessor of word_B if and only if we can insert exactly one letter anywhere in word_A without changing the order of the other characters to make it equal to word_B.
#
# For example, "abc" is a predecessor of "abac", while "cba" is not a predecessor of "bcad".
#
# A word chain is a sequence of words [word_1, word_2, ..., word_k] with k >= 1, where word_1 is a predecessor of word_2, word_2 is a predecessor of word_3, and so on. A single word is trivially a word chain with k == 1.
#
# Return the length of the longest possible word chain with words chosen from the given list of words.
#
# Example 1:
#
# Input: words = ["a","b","ba","bca","bda","bdca"]
# Output: 4
# Explanation: One of the longest word chains is ["a","ba","bda","bdca"].
#
# Example 2:
#
# Input: words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]
# Output: 5
# Explanation: All the words can be put in a word chain ["xb", "xbc", "cxbc", "pcxbc", "pcxbcf"].
#
# Example 3:
#
# Input: words = ["abcd","dbqca"]
# Output: 1
# Explanation: The trivial word chain ["abcd"] is one of the longest word chains.
# ["abcd","dbqca"] is not a valid word chain because the ordering of the letters is changed.
#
# Constraints:
#
#     1 <= words.length <= 1000
#     1 <= words[i].length <= 16
#     words[i] only consists of lowercase English letters.
#
# ---
# Learning: correct solution, wrong approach
# LEETCODE: Wrong Answer (83/86 cases)

# mu 0.14

class Solution
  def isChain(a, b)
    len b == len a + 1 and lcs(a, b) == len a
  
  def longestStrChain(words: [str]) -> int
    words.sort(key= x -> len x)
    print(words)
    wordsLen = {:list: len(x) <- x for x in words}
    print(wordsLen)
    dp = {: -> int(1)}
    for word in words
      if len word > 1
        for shorter_word in wordsLen[len word -1]
          if self.isChain(shorter_word, word)
            dp[word] = max(dp[shorter_word] + 1, dp[word])
    max(dp.values(), default=1)

sol = Solution()


assert sol.isChain('a', 'b') == false
assert sol.isChain('a', 'ba') == true
assert sol.isChain('ba', 'bda') == true
assert sol.isChain('bda', 'bdca') == true
assert sol.isChain('xbc', 'cxbc') == true
assert sol.isChain('abcd', 'dbqca') == false
assert sol.isChain('abcd', 'dbqca') == false


assert sol.longestStrChain(["bdca","bda","ca","dca","a"]) == 4
assert sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca']) == 4
assert sol.longestStrChain(['xbc', 'pcxbcf', 'xb', 'cxbc', 'pcxbc']) == 5
assert sol.longestStrChain(['abcd', 'dbqca']) == 1
assert sol.longestStrChain(['a']) == 1
assert sol.longestStrChain(['a', 'aa', 'aaa', 'aaaa', 'aaaaa']) == 5
assert sol.longestStrChain(['a', 'b', 'c', 'd']) == 1
assert sol.longestStrChain(['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef']) == 6
assert sol.longestStrChain(['a', 'ab', 'ac', 'abc', 'abd', 'abcd', 'abce']) == 4
assert sol.longestStrChain(['z' * i for i in 1..<17]) == 16
assert sol.longestStrChain(['a' * 16, 'a' * 15, 'a' * 14]) == 3
assert sol.longestStrChain(['a', 'ab', 'abc', 'abd', 'abdd', 'abddd', 'abdddd']) == 6
assert sol.longestStrChain(['a', 'ba', 'bca', 'bdca', 'bdcaa']) == 5
assert sol.longestStrChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca', 'bdcaa', 'bdcaaa']) == 6
assert sol.longestStrChain(['a' * i for i in 1..<1001 if i <= 16]) == 16
assert sol.longestStrChain(['a' * 16] * 1000) == 1




print(sol.longestStrChain(["klmnowx","abcdefgiklmno","fgij","bcfghijklmno","fgjpqrst","uy","abceklmnouvw","pqrstuwy","fghijlno","mnouvwxy","klmnopqt","klmnopqrstuy","aeuvw","muvw","abcdeklmnow","fhijpqrst","mpqrst","klmnoprt","fghijklno","abcdelmo","klnuvwxy","klmnopst","abcdeklmnov","fghj","luvwxy","ghklmnopqrst","pqrstwx","abcdklmno","cdefghij","pqrs","efghijklmno","fghjklmno","adeklmno","rs","kuvwxy","ghij","befghijklmno","ln","hijklmnopqrst","ghpqrst","fgiklmnopqrst","pqrtuvwxy","pqrsty","jklmnopqrst","lnouvwxy","klmnoqsuvwxy","abcdeghklmno","fi","fghijlnpqrst","abdklmnouvw","uwx","abcdekln","klmno","abcdekn","abcdemuvw","pqs","fghijpqt","klmnopqrstuw","n","nopqrstuvwxy","abcdefghj","fghiklmnopqrst","klmnorst","abcdemnouvw","fgh","pqt","abfghij","o","nouvw","abcdklmnouvw","abeklmno","abcden","klmnopqrstwxy","q","fghijklmnoprt","klmnovx","abceuvw","klmnopsuvwxy","hj","abcdefgh","fhjklmno","klmnoquvwxy","wxy","klmnopqrstuvwy","kln","abcdegklmno","mno","gklmno","klnouvw","fghijklmnoqr","fghijpqrst","mnuvwxy","ghipqrst","klmnoqrtuvwxy","acdfghij","uwy","fghjklmnopqrst","mnpqrstuvwxy","abcdeknouvw","abcdefghijklmno","klmnorsuvwxy","abcdeh","klmnost","iklmnopqrst","abcdegijklmno","fghijklmopqrst","fghijklmnors","pqrstux","abcdefghijlm","abcdem","klmn","opqrst","ghjklmnopqrst","cdfghij","kluvwxy","ceklmno","abcdeghijklmno","lmo","bklmno","fghijs","cdeklmnouvw","abcdeknuvw","cdklmnouvw","abcdeklmnovw","klmnopr","fghijklmnopqrst","klmnopqtuvwxy","abcdefhijklmno","abcdeuv","abcdefhklmno","x","abcdeouvw","fjklmno","a","klmnopqrstuv","abdklmno","fghijlm","bcefghijklmno","quvwxy","fghi","klmnopqrstuwx","r","klmnuvw","kn","abcdeklmn","abcdeklmno","ps","klmnoqrt","pstuvwxy","klmnopqrsty","lmn","d","abcdefghijmo","fghijmnopqrst","ghiklmno","mouvwxy","abcdeghj","fghijklmnopr","kmnouvwxy","fghijklmnopqst","klmnox","nouvwxy","adefghijklmno","kmo","klmnovy","klmnopqrstuvwxy","cde","y","klmnouy","fgklmnopqrst","nuvwxy","kluvw","abcdefghijkno","abcdekl","fghijno","ceuvw","abcdelo","bcdklmno","gij","abcdeijklmno","klmnopqrt","abcdeklm","pqruvwxy","klnuvw","fijklmno","knpqrstuvwxy","fghijklmnor","ace","abcdekluvw","deklmnouvw","lpqrstuvwxy","abcdefhiklmno","fijpqrst","klmnopqrstvwy","mn","kmpqrst","ipqrst","fghijkmnpqrst","uvxy","bklmnouvw","fghijkmnopqrst","fghijklnopqrst","kopqrstuvwxy","pqrstuwxy","abdeuvw","acefghij","jklmno","k","fghijqs","abcdefghijno","fghijklmnort","adeuvw","vwx","gjklmno","hi","abcdefghijm","nuvw","fklmnopqrst","abcdehklmno","fghijklmnoqrt","klmnoruvwxy","abcdemnuvw","klmnovw","klmnopqrstvw","klmnoqtuvwxy","klmnoy","wx","ouvwxy","lmopqrst","fghjpqrst","lnuvwxy","vy","abdfghijklmno","kmnouvw","uvy","klmnoqst","klmnort","pqrstuxy","qs","lopqrstuvwxy","mnouvw","abdeklmno","abcdelnouvw","pruvwxy","qrsuvwxy","cklmno","bc","acdfghijklmno","j","fghijpqs","fghijknopqrst","fgijklmno","fghijnopqrst","mpqrstuvwxy","knopqrst","acdeuvw","lnouvw","fghijklmn","klmnouvxy","abcdefghiklmno","abcdefghij","hij","abcdekuvw","klmnopqs","aklmnouvw","acdefghijklmno","cfghij","fghijpqst","cfghijklmno","abcdefhi","kmouvwxy","pquvwxy","pqrstuy","pqrstuwx","ce","klmnopqrstv","deklmno","klmnouvw","abcdeno","fghijkmo","knouvwxy","fpqrst","hklmno","fghijkmopqrst","abcdefghjklmno","kmpqrstuvwxy","dklmnouvw","abcdefghijkmo","abcdel","giklmnopqrst","buvw","klmo","klmnoqrsuvwxy","uvwy","abcdeluvw","klmnostuvwxy","bceklmno","fghijm","defghijklmno","ijklmno","pqr","abcduvw","fghijklmnopqt","hijklmno","klmnoprsuvwxy","aeklmno","lo","klmnouxy","cdklmno","fghijpr","muvwxy","lmnouvwxy","abce","kmnopqrst","pt","klmnoptuvwxy","abde","abcdeghiklmno","klmnopqsuvwxy","klmnouvx","efghij","klmnouwy","bceklmnouvw","klmnuvwxy","ad","klmnoux","gjpqrst","abcdegij","fghijkpqrst","fghijlmnopqrst","abcdefj","fghijklmnops","fghijklmnoqs","ghi","fghijqst","abcdemo","abcdefghijkl","fghklmnopqrst","no","klmnopqrstuwxy","klmnopqrstvwx","abcdeklmnou","abdefghijklmno","klmnopqrstxy","acfghij","pqrstuvwy","kuvw","abcdehi","de","fghijpq","lmuvwxy","abcdelmouvw","abdfghij","knuvwxy","acde","cuvw","uw","kmopqrstuvwxy","abcfghij","fghij","abcdeklmo","abcdehij","abcdek","fghijklmnoqrst","pqrstvx","klmnopqrstvx","abc","klmnoqrstuvwxy","acklmnouvw","afghijklmno","abcdeklmnuvw","abcdei","fgiklmno","klmnopqrstuvw","abcklmnouvw","abcdelmnuvw","abcdehj","abcdefghijlo","fghpqrst","acfghijklmno","abcdeg","klpqrst","klmouvw","bdfghijklmno","aefghijklmno","fijklmnopqrst","fghijps","fghijklnpqrst","fghijklmnop","fklmno","klmnopqrstw","abcdfghijklmno","fj","lnopqrst","fghijkmpqrst","fghijlnopqrst","ux","fgjklmno","fghijklmnopqr","abcdeghjklmno","abcdefghijkmn","abcdegiklmno","abcdefiklmno","acdeklmno","klmnops","fghijklmnopqrt","fghijklmnoqt","abcdegj","acdklmno","abcdeghi","abcdelmuvw","abcdefg","fghijkl","gjklmnopqrst","hipqrst","klmnopqstuvwxy","lnuvw","ghijpqrst","pqrstuvwxy","klmnovwx","klmnoqstuvwxy","bcklmnouvw","abdeklmnouvw","fghijklmnopq","abcdefghijk","abcdefghijklno","fiklmnopqrst","klmnopq","npqrstuvwxy","klmnopqrstwx","abcdefi","lpqrst","ghijklmnopqrst","bd","bcuvw","hjklmnopqrst","adfghijklmno","klmnosuvwxy","louvwxy","bce","gpqrst","fghijklmnot","wy","pqrstvwxy","fghijkln","lmouvw","gi","fghijn","fhklmnopqrst","ghj","klpqrstuvwxy","abcdefgklmno","fghijlmo","fghijo","fhpqrst","klmnoprs","abcefghij","abcdeklno","abcdefghijlmno","kmnpqrst","fghijklmnoq","abcdefhij","fghijklmnopt","klmnopt","abcdefklmno","abcdelno","pqrstw","fghijlopqrst","bfghij","abuvw","abcdefghijln","ac","aefghij","prs","lmnopqrstuvwxy","abcdefghijn","klmnopqrstux","luvw","giklmno","kpqrst","jpqrst","fghijrt","fghijlo","abcdefij","fghijklmnorst","fghijqrst","tuvwxy","fghijlmopqrst","klmnouwxy","bdeuvw","fghijprt","klmnoprst","pqrstuvy","fghijpqrt","fgj","pqrstvxy","abdefghij","abcdegh","abefghij","lno","klmnopuvwxy","klmnouvwxy","fghijrst","cd","euvw","hijpqrst","pqrst","klopqrst","gijpqrst","klmnopqrs","fghijk","klopqrstuvwxy","rtuvwxy","klmnorstuvwxy","stuvwxy","abcdevw","cdefghijklmno","bdeklmno","pqstuvwxy","fghipqrst","fghijpst","kmn","mo","abcdeuw","qst","fghijklmnost","klnopqrst","abcdekm","abcdefgj","klmnopqrstuvy","kouvw","abcdelmnouvw","abefghijklmno","fgipqrst","klm","klmnopstuvwxy","abcdekmno","fghijmno","pqrstvw","kmouvw","cdeklmno","st","fij","fhiklmno","abcdefghklmno","lmnuvwxy","klmnovwy","klmnow","mnuvw","fghijklmnpqrst","klmnoxy","fghklmno","b","lopqrst","pqrstuvw","abcdekmouvw","abcdeklmnouw","acduvw","klmnoq","bde","pqrstxy","qrs","bcdeklmnouvw","abcdekmo","abcdefghijkn","kno","abcdefghijklm","abcdefgij","kmopqrst","kmnuvwxy","pqrstuvwx","fghijkmn","acdefghij","fghijmn","qr","l","kmnopqrstuvwxy","abcdefghijl","afghij","auvw","abcdew","klmnopqrstwy","adfghij","abcdeghij","lmopqrstuvwxy","abcdefghijklmn","uvx","km","abcdefijklmno","abcdeij","pq","lnpqrst","bdfghij","abcdefhj","mopqrstuvwxy","fghijklmnopqs","fghijqt","ade","abcdejklmno","fghijklmpqrst","pqrstuvxy","mouvw","mopqrst","lmnopqrst","abcdefhjklmno","acdklmnouvw","bcklmno","nopqrst","qrt","fghijlmnpqrst","pqrstuv","klmnos","pqrstwxy","fgjklmnopqrst","pqrstuw","klmnopqrstuvxy","fhijklmno","abcdekmnuvw","ghjklmno","klmnoprtuvwxy","abcdefghijlmn","klmouvwxy","abcdegjklmno","p","hiklmnopqrst","rstuvwxy","gh","cdfghijklmno","klmnou","iklmno","klmnopqrstvxy","lmpqrstuvwxy","prtuvwxy","klmnovwxy","pqst","klmnortuvwxy","lmnpqrstuvwxy","fghijmpqrst","ghiklmnopqrst","klmpqrst","klmnoprstuvwxy","ghklmno","fghijopqrst","klmnoqruvwxy","abcdeklmouvw","ae","abcfghijklmno","vw","fghijr","kmnpqrstuvwxy","fghijklpqrst","vwxy","uxy","cklmnouvw","abcdefghijkm","uvw","bcd","bcefghij","abcdeiklmno","klmnot","cduvw","fghijmo","eklmnouvw","klmnopqrstuwy","kmnuvw","lmouvwxy","abcdefghijlmo","cefghij","klmnoqs","klmnouwx","kmuvwxy","ceklmnouvw","fghijklmnoqrs","abduvw","abceklmno","ghijklmno","abcdefghijmn","bcdfghij","pqrstvwx","fghijlpqrst","gijklmnopqrst","abcdelnuvw","pqrstvwy","pr","fghijklmnos","c","fghijklmno","abcdefghijkmno","abcuvw","abcdev","abeuvw","pqrstuvx","klo","fghijln","klmnpqrstuvwxy","abcdefghijlno","fghijklmnopst","acd","gipqrst","w","abcdenuvw","deuvw","abcdeklmnouvw","fg","cdeuvw","lmnuvw","abcdenouvw","klmnoqt","hklmnopqrst","klmnouvwy","gijklmno","klmnopqrst","fghijmopqrst","kmno","f","uv","fhij","knuvw","klmnor","klnouvwxy","bcdeuvw","bdklmno","abklmnouvw","abcdehjklmno","bcde","fghijklmo","abcdefghijklmo","ko","abcdeklmuvw","bcdefghijklmno","beuvw","qstuvwxy","aeklmnouvw","h","t","kmuvw","fhi","fjklmnopqrst","hiklmno","fhipqrst","qrtuvwxy","abcdeklnuvw","fghijqrt","pqrstx","bdefghijklmno","gj","abcdelmno","abcdefjklmno","fhjpqrst","klnpqrst","fgijklmnopqrst","abcdelm","fghijrs","klmnouw","fhklmno","abcdeln","fgijpqrst","fghijklmnoqst","abeklmnouvw","klmuvw","i","lmno","fghijklo","fghijkm","g","adklmnouvw","be","abcdefgjklmno","prst","puvwxy","qrstuvwxy","klmnov","klmnopqrstuvwx","acefghijklmno","fghijpqrs","fhj","abklmno","abcd","fiklmno","ijpqrst","fghijnpqrst","lmnouvw","suvwxy","knouvw","duvw","fghijkmno","bdefghij","aceklmno","fgklmno","fghijst","adefghij","fghijklmnopqrs","bcdefghij","abcdefghijko","klmnotuvwxy","klmnopruvwxy","klmnovxy","qtuvwxy","fhjklmnopqrst","klmnoqrst","prt","fghijt","uvwx","abcdekmnouvw","dfghij","abcdehiklmno","klmnopqrstu","adeklmnouvw","abcdefghijmno","klmnopquvwxy","abcdefghijkln","mnpqrst","fghijlmn","lnopqrstuvwxy","pqrt","fghijpt","abcde","ij","bcdklmnouvw","fghijkn","pst","bdklmnouvw","abcdeko","fh","fjpqrst","fghijqr","beklmno","fghijklopqrst","lmuvw","klouvw","fghijpqr","abcdegi","psuvwxy","klnopqrstuvwxy","abcdelmn","fhiklmnopqrst","fghijprst","lnpqrstuvwxy","qruvwxy","aduvw","abcdekmuvw","adklmno","abcdeu","cefghijklmno","lm","hjklmno","abcdefghijklo","klmnoqrs","fghijko","ouvw","pqrstu","mnopqrst","louvw","prsuvwxy","abcdekno","klmnopqruvwxy","kpqrstuvwxy","abcdefgijklmno","klmnors","abcdefghijo","npqrst","knopqrstuvwxy","vx","fghijqrs","klmnopqrstuxy","u","aceuvw","klmnopqrtuvwxy","uvwxy","fipqrst","klmnowxy","befghij","gklmnopqrst","abe","mnopqrstuvwxy","fghijklmnoprs","abcdeo","eklmno","fgi","fghijlmpqrst","qt","abcdefghi","bcduvw","bduvw","klouvwxy","kouvwxy","fghiklmno","abcdemno","pqsuvwxy","ab","klmnopqrstvwxy","pqrstv","abfghijklmno","beklmnouvw","fghijklm","pqrsuvwxy","acdeklmnouvw","vwy","ghjpqrst","fghijl","klmnopqrstvy","abcdelouvw","fhijklmnopqrst","klmpqrstuvwxy","abcdef","bcfghij","fghijkno","kopqrst","rsuvwxy","abcdekmn","aklmno","dfghijklmno","abcdeklouvw","klmnpqrst","abcdeklmnouv","knpqrst","aceklmnouvw","kl","fghijprs","rt","klmnopqrsuvwxy","bfghijklmno","klmnouv","abcdefh","s","klmnouvwx","fghijp","uwxy","fghijq","klmnoqr","vxy","fgpqrst","fghijlmno","defghij","pqtuvwxy","dklmno","klno","klmnowy","abcdemn","abcdeklnouvw","ptuvwxy","abcdehijklmno","acuvw","bcdfghijklmno","abcdemouvw","abcdefgi","opqrstuvwxy","v","lmpqrst","abcdeuvw","abcdekouvw","qrst","klmopqrstuvwxy","prstuvwxy","lmnpqrst","pqrstvy","abcdfghij","klmnop","ijklmnopqrst","klnpqrstuvwxy","klmnopqr","xy","abcdeklo","abd","klmnouvy","klmuvwxy","abcefghijklmno","fghijkopqrst","fghijklmnoprst","ruvwxy","m","e","abcdej","hpqrst","bceuvw","fghijmnpqrst","pqrstwy","klmnopqrstx","qsuvwxy","fghijknpqrst","bcdeklmno","klmopqrst","bdeklmnouvw","klmnopqst","klmnopqrstuvx","acklmno","hjpqrst","abcklmno","rst"]))


# FAILED: walked away after 62m 48s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
