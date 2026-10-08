# combo chain: backend, problem 4 of 10. Run `make combos backend` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend.json.
"""
URL: https://leetcode.com/problems/design-authentication-manager/description/?envType=problem-list-v2&envId=vn57k9wr

1797. Design Authentication Manager

There is an authentication system that works with authentication tokens. For each session, the user will receive a new authentication token that will expire timeToLive seconds after the currentTime. If the token is renewed, the expiry time will be extended to expire timeToLive seconds after the (potentially different) currentTime.

Implement the AuthenticationManager class:

- AuthenticationManager(int timeToLive) constructs the AuthenticationManager and sets the timeToLive.
- generate(string tokenId, int currentTime) generates a new token with the given tokenId at the given currentTime in seconds.
- renew(string tokenId, int currentTime) renews the unexpired token with the given tokenId at the given currentTime in seconds. If there are no unexpired tokens with the given tokenId, the request is ignored, and nothing happens.
- countUnexpiredTokens(int currentTime) returns the number of unexpired tokens at the given currentTime.

Note that if a token expires at time t, and another action happens on time t (renew or countUnexpiredTokens), the expiration takes place before the other actions.

Example 1:

Input
["AuthenticationManager","renew","generate","countUnexpiredTokens","generate","renew","renew","countUnexpiredTokens"]
[[5],["aaa",1],["aaa",2],[6],["bbb",7],["aaa",8],["bbb",10],[15]]

Output
[null,null,null,1,null,null,null,0]

Explanation
AuthenticationManager authenticationManager = new AuthenticationManager(5); // Constructs the AuthenticationManager with timeToLive = 5 seconds.
authenticationManager.renew("aaa", 1); // No token exists with tokenId "aaa" at time 1, so nothing happens.
authenticationManager.generate("aaa", 2); // Generates a new token with tokenId "aaa" at time 2.
authenticationManager.countUnexpiredTokens(6); // The token with tokenId "aaa" is the only unexpired one at time 6, so return 1.
authenticationManager.generate("bbb", 7); // Generates a new token with tokenId "bbb" at time 7.
authenticationManager.renew("aaa", 8); // The token with tokenId "aaa" expired at time 7, and 8 >= 7, so at time 8 the renew request is ignored, and nothing happens.
authenticationManager.renew("bbb", 10); // The token with tokenId "bbb" is unexpired at time 10, so the renew request is fulfilled and now the token will expire at time 15.
authenticationManager.countUnexpiredTokens(15); // The token with tokenId "bbb" expires at time 15, and the token with tokenId "aaa" expired at time 7, so currently no token is unexpired, so return 0.

Constraints:

    1 <= timeToLive <= 10^8
    1 <= currentTime <= 10^8
    1 <= tokenId.length <= 5
    tokenId consists only of lowercase letters.
    All calls to generate will contain unique values of tokenId.
    The values of currentTime across all the function calls will be strictly increasing.
    At most 2000 calls will be made to all functions combined.

---

LEETCODE: Wrong Answer (72/91 cases)
"""


class AuthenticationManager:

    def __init__(self, timeToLive: int):
        self.ttl = timeToLive
        self.tokens = {}

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.tokens[tokenId] = currentTime

    def renew(self, tokenId: str, currentTime: int) -> None:
        if tokenId in self.tokens:
            self.tokens[tokenId] = currentTime

    def countUnexpiredTokens(self, currentTime: int) -> int:
        return len([x for x in self.tokens if self.tokens[x] + self.ttl > currentTime])


sol = AuthenticationManager(5)

sol.renew("aaa", 1)  # No token exists with tokenId "aaa" at time 1, so nothing happens.
sol.generate("aaa", 2)  # Generates a new token with tokenId "aaa" at time 2.
print(sol.countUnexpiredTokens(6))  # 1
sol.generate("bbb", 7)  # Generates a new token with tokenId "bbb" at time 7.
sol.renew("aaa", 8)  # The token with tokenId "aaa" expired at time 7, so renew ignored.
sol.renew("bbb", 10)  # The token with tokenId "bbb" is unexpired at time 10, renewed.
print(sol.countUnexpiredTokens(15))  # 0

# Assertions for the example
am = AuthenticationManager(5)
am.renew("aaa", 1)
am.generate("aaa", 2)
assert am.countUnexpiredTokens(6) == 1
am.generate("bbb", 7)
am.renew("aaa", 8)
am.renew("bbb", 10)
assert am.countUnexpiredTokens(15) == 0

assert AuthenticationManager(1).countUnexpiredTokens(1) == 0
