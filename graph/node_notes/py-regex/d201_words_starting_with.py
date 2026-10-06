# REFERENCE: d201 Words Starting With
class Solution:
    def words_starting_with(self, s, c):
        return re.findall(rf"\b{c}[a-z]*", s)
