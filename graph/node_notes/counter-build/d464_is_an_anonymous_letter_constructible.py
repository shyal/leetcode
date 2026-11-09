# REFERENCE: d464 EPI 12.2 Is an anonymous letter constructible?
class Solution:
    def is_letter_constructible_from_magazine(self, letter_text, magazine_text):
        need = Counter(letter_text)
        for c in magazine_text:
            if c in need:
                need[c] -= 1
                if need[c] == 0:
                    del need[c]
                    if not need:
                        break
        return not need
