# REFERENCE: d401 EPI 6.4 Replace and remove
class Solution:
    def replace_and_remove(self, size, s):
        write = a_count = 0
        for read in range(size):
            if s[read] == "a":
                a_count += 1
            if s[read] != "b":
                s[write] = s[read]
                write += 1
        n = write + a_count
        read, write = write - 1, n - 1
        while read >= 0:
            if s[read] == "a":
                s[write - 1] = s[write] = "d"
                write -= 2
            else:
                s[write] = s[read]
                write -= 1
            read -= 1
        return n
