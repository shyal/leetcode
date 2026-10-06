REFERENCE: d228 Back Pressure
SOURCE: System Design Primer, "Back pressure" https://github.com/donnemartin/system-design-primer#back-pressure

REQUIRED
- A queue that grows significantly can become larger than memory, which
  causes cache misses, disk reads and slower performance.
- Back pressure limits the queue size, which keeps a high throughput rate
  and good response times for the jobs already in the queue.
- Once the queue is full, clients get a server busy or HTTP 503 status code,
  telling them to try again later.
- Clients retry the request later, perhaps with exponential backoff.
