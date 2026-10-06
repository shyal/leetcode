REFERENCE: d234 Token Bucket
SOURCE: Stripe, "Scaling your API with rate limiters" https://stripe.com/blog/rate-limiters

REQUIRED
- Each user has a bucket of tokens; every request removes one token from
  that user's bucket.
- Tokens are added back to the bucket slowly, at a steady rate.
- If the bucket is empty, the request is rejected.
- It lets a user briefly burst above the cap, for sudden spikes in usage.
- The buckets are kept in a central store shared by all servers; Stripe uses
  Redis.
- The limiter must fail open: if its code has a bug or the store is down,
  requests are not affected and the API stays functional.
- A limited client receives HTTP 429, Too Many Requests.

ALSO TRUE
- A rate limiter decides per user; a load shedder decides on the state of
  the whole system and answers 503.
- Build in a kill switch to disable a limiter, and dark launch each one to
  see what it would block.
- A concurrent requests limiter caps requests in progress instead of
  requests per second.
