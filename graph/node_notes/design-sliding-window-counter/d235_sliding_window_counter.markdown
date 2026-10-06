REFERENCE: d235 Sliding Window Counter
SOURCE: Cloudflare, "How we built rate limiting capable of scaling to millions of domains" https://blog.cloudflare.com/counting-things-a-lot-of-different-things/

REQUIRED
- rate = previous count * ((period - elapsed) / period) + current count.
- 42 * ((60 - 15) / 60) + 18 = 42 * 0.75 + 18 = 49.5 requests.
- 49.5 is under 50, so the next request is allowed; one more request after
  it is not.
- It assumes a constant rate of requests during the previous period, so the
  result is an approximation.
- A fixed window counter resets at the start of each period, which lets
  regular traffic spikes through the limiter.
- Only two numbers are stored per counter: the previous period's count and
  the current one.

ALSO TRUE
- Incrementing is one atomic INCR command.
- Storing a timestamp per request is more accurate but has huge processing
  and memory requirements.
- The leaky bucket is accurate too, but has two parameters, average rate and
  burst, that are hard to tune.
- On 400 million requests, 0.003% were wrongly allowed or limited.
