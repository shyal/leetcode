REFERENCE: d236 Charge Once
SOURCE: Stripe, "Designing robust and predictable APIs with idempotency" https://stripe.com/blog/idempotency

REQUIRED
- The initial connection can fail as the client tries to connect.
- The call can fail midway, while the server is fulfilling the operation.
- The call can succeed, but the connection breaks before the server can tell
  the client.
- An idempotent endpoint can be called any number of times while its side
  effects occur only once.
- The client generates a unique ID for the one operation and sends it with
  the request; on a failure it retries with the same ID.
- After a connection failure: the server sees the ID for the first time and
  processes the request normally.
- After a failure midway: the server picks the work up and carries it
  through; if the first attempt was rolled back in an ACID database, the
  whole request is safe to retry.
- After a lost response: the server replies with the cached result of the
  successful operation.

ALSO TRUE
- Stripe takes the key in an Idempotency-Key header on mutating, POST,
  endpoints.
- By HTTP semantics PUT and DELETE are idempotent.
