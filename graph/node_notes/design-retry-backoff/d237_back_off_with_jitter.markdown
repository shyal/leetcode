REFERENCE: d237 Back Off With Jitter
SOURCE: Stripe, "Designing robust and predictable APIs with idempotency" https://stripe.com/blog/idempotency

REQUIRED
- The client waits a brief initial time after the first failure, then a time
  proportional to 2^n, where n is the number of failures so far.
- This keeps clients from hammering a downed server and adding to the
  problem.
- Thundering herd: when a server problem makes many clients fail at about
  the same time, their retry schedules line up, and the retries hit the
  troubled server together even with backoff.
- Jitter is a random amount added to each client's wait time; it spaces the
  requests out across clients and gives the server room to recover.
