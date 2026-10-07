REFERENCE: d252 Pastebin Scaled
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- Scaled: a Memory Cache handles the popular content and the uneven traffic;
  SQL Read Replicas handle the cache misses; a single SQL Write Master-Slave
  handles 4 writes per second.

ALSO TRUE
- Page analytics need not be realtime: MapReduce over the Web Server logs
  gives the hit counts.
- Scale iteratively: benchmark, profile for bottlenecks, address them weighing
  alternatives, repeat.
