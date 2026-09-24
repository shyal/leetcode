# REFERENCE: d11 Count Smaller Values
def smallerThanEach(nums: [int]) -> [int]
  count = table(101, fill = 0)
  for x in nums
    count[x] += 1
  below = [0, *scan(+, count)]
  [below[x] for x in nums]
