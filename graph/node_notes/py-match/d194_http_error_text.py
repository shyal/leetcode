# REFERENCE: d194 HTTP Error Text
class Solution:
    def http_error(self, status):
        match status:
            case 400:
                return "Bad request"
            case 401 | 403:
                return "Not allowed"
            case 404:
                return "Not found"
            case 418:
                return "I'm a teapot"
            case _:
                return "Something's wrong with the internet"
