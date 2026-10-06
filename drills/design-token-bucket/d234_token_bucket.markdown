DRILL: Token Bucket
TRAINS: design-token-bucket

Describe the token bucket algorithm: what a request does to the bucket, how
the bucket refills, and what happens when it is empty. Say what it allows
that a strict requests-per-second cap does not. State where the buckets are
kept when many servers take requests, what the limiter must do when that
store is down, and which HTTP status a limited client receives.

REQUIRED: take a token, refill at a steady rate, reject when empty, the
burst, a central store, failing open, 429. Rejecting every request when the
store is down is the fail.

## Answer
