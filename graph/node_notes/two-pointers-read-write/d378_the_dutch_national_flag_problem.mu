# REFERENCE: d378 EPI 5.1 The Dutch national flag problem
class Solution
  def dutch_flag_partition(pivot_index: int, A: [int])
    pivot = A[pivot_index]
    lo, mid, hi = 0, 0, len(A)
    while mid < hi
      if A[mid] < pivot
        A[lo], A[mid] = A[mid], A[lo]
        lo += 1
        mid += 1
      elif A[mid] == pivot
        mid += 1
      else
        hi -= 1
        A[mid], A[hi] = A[hi], A[mid]
