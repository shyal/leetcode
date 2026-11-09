# REFERENCE: d468 EPI 12.6 Find the smallest subarray covering all values
class Solution
  def find_smallest_subarray_covering_set(paragraph: [str], keywords: {str}) -> (int, int)
    best, inside, left = (-1, -1), {:int}, 0
    for >right, word in paragraph
      if word in keywords
        inside[word] += 1
      while len(inside) == len(keywords)
        if best[0] < 0 or right - left < best[1] - best[0]
          best = (left, right)
        word = paragraph[left]
        if word in keywords
          inside[word] -= 1
          if inside[word] == 0
            del inside[word]
        left += 1
    best
