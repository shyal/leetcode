REFERENCE: d214 In Front Of One Server
SOURCE: System Design Primer, "Reverse proxy (web server)" https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server

REQUIRED
- A reverse proxy is a web server that centralises internal services and
  provides unified interfaces to the public.
- It forwards a client's request to a server that can fulfil it, then
  returns that server's response to the client.
- Four benefits out of: increased security, hiding backend servers,
  blacklisting IPs, limiting connections per client; increased scalability
  and flexibility, since clients see only the proxy's IP; SSL termination;
  compression of responses; caching of responses; serving static content
  directly.
- A reverse proxy is useful even with one web or application server; a load
  balancer is useful when there are several servers serving the same
  function.
- One disadvantage out of: it increases complexity; a single reverse proxy
  is a single point of failure, and configuring several adds more
  complexity.

ALSO TRUE
- NGINX and HAProxy support both layer 7 reverse proxying and load
  balancing.
