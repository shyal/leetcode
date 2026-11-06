# REFERENCE: d355 Sentence Reverse
class Solution
  def reverse_words(arr: [str]) -> [str]
    def flip(lo: int, hi: int) -> none
      while lo < hi
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1
    flip(0, len arr - 1)
    start = 0
    for i in 0..len arr
      if i == len arr or arr[i] == ' '
        flip(start, i - 1)
        start = i + 1
    arr
