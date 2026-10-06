DRILL: Charge Once
TRAINS: design-idempotency-key

A client calls an endpoint that charges a card, and the call fails. Name the
three points at which a call between two nodes can fail. Define an
idempotent endpoint. Describe the idempotency key: who generates it, when
the same key is sent again, and what the server does on the retry in each of
the three cases.

REQUIRED: three failure points, the definition, the client-generated key
reused on retry, the server's action in each case. Generating a new key for
the retry is the fail.

## Answer
