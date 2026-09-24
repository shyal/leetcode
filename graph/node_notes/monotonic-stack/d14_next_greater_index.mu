# REFERENCE: d14 Next Greater Index
def nextGreaterIndex(nums: [int]) -> [int]
  res = table(len(nums), fill = -1)
  stack = []
  for i, x in nums
    while stack and nums[stack[-1]] < x
      res[stack .] = i
    stack <- i
  res
