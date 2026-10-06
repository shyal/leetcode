REFERENCE: d208 Active Passive Active Active
SOURCE: System Design Primer, "Availability patterns: fail-over" https://github.com/donnemartin/system-design-primer#fail-over

REQUIRED
- Active-passive: heartbeats are sent between the active server and the
  passive server on standby. If the heartbeat is interrupted, the passive
  server takes over the active's IP address and resumes service.
- Only the active server handles traffic.
- The downtime depends on whether the passive server is already running, hot
  standby, or must start up, cold standby.
- Active-active: both servers manage traffic and spread the load between
  them.
- In active-active, DNS must know the public IPs of both servers when they
  are public-facing; application logic must know about both when they are
  internal.
- Disadvantage: fail-over adds more hardware and more complexity.
- Disadvantage: data can be lost if the active system fails before newly
  written data is replicated to the passive.

ALSO TRUE
- Active-passive is also called master-slave failover, and active-active
  master-master failover.
