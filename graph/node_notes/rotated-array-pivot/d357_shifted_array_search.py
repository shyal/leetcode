# REFERENCE: d357 Shifted Array Search
class Solution:
    def shifted_arr_search(self, shiftArr, num):
        lo, hi = 0, len(shiftArr) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if shiftArr[0] <= shiftArr[mid]:
                if shiftArr[0] <= num <= shiftArr[mid]:
                    hi = mid
                else:
                    lo = mid + 1
            else:
                if shiftArr[mid] < num <= shiftArr[-1]:
                    lo = mid + 1
                else:
                    hi = mid
        return lo if shiftArr[lo] == num else -1
