REFERENCE: d210 Name To Address
SOURCE: System Design Primer, "Domain name system" https://github.com/donnemartin/system-design-primer#domain-name-system

REQUIRED
- DNS translates a domain name such as www.example.com to an IP address.
- NS record: the DNS servers for the domain or subdomain.
- MX record: the mail servers that accept messages.
- A record: points a name to an IP address.
- CNAME: points a name to another name, or to an A record.
- Lower level DNS servers, the browser and the OS cache mappings, so an
  answer can be stale after a change; the time to live, TTL, sets how long a
  result is cached.
- Two disadvantages out of: a lookup adds a slight delay, mitigated by
  caching; DNS server management is complex and is generally done by
  governments, ISPs and large companies; DNS services come under DDoS
  attack, which keeps users from reaching sites.

ALSO TRUE
- Managed DNS services can route by weighted round robin, by latency or by
  geolocation.
- Weighted round robin keeps traffic away from servers under maintenance,
  balances clusters of different sizes, and allows A/B testing.
