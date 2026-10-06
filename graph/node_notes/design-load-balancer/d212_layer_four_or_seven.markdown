REFERENCE: d212 Layer Four Or Seven
SOURCE: System Design Primer, "Load balancer" https://github.com/donnemartin/system-design-primer#load-balancer

REQUIRED
- It prevents requests from going to unhealthy servers.
- It prevents overloading resources.
- It helps eliminate a single point of failure.
- Layer 4 reads the transport layer: the source and destination IP addresses
  and ports in the header, not the contents of the packet. It forwards
  packets with network address translation and needs less time and
  computing.
- Layer 7 reads the application layer: the header, the message and the
  cookies. It terminates the traffic, reads the message, decides, then opens
  a connection to the chosen server. It is more flexible and costs more time
  and computing.
- Two disadvantages out of: it can become a performance bottleneck if it
  lacks resources or is badly configured; it increases complexity; a single
  load balancer is itself a single point of failure, and several of them add
  more complexity.

ALSO TRUE
- A layer 7 load balancer can send video traffic to servers that host videos
  and billing traffic to security-hardened servers.
- Other benefits: SSL termination and session persistence with cookies.
- Routing methods include random, least loaded, session or cookies, and
  round robin or weighted round robin.
- Load balancers themselves are set up in active-passive or active-active
  pairs.
