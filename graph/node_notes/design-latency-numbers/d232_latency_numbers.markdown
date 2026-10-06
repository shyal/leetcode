REFERENCE: d232 Latency Numbers
SOURCE: System Design Primer, "Latency numbers every programmer should know" https://github.com/donnemartin/system-design-primer#latency-numbers-every-programmer-should-know

REQUIRED
- Main memory reference: 100 ns.
- Round trip within the same datacenter: 500 us, 0.5 ms.
- HDD seek: 10 ms.
- Read 1 MB sequentially from memory: 250 us.
- Read 1 MB sequentially from SSD: 1 ms.
- Read 1 MB sequentially from HDD: 30 ms.
- Packet from California to the Netherlands and back: 150 ms.
- Sequential read rates: HDD 30 MB/s, SSD 1 GB/s, main memory 4 GB/s.

ALSO TRUE
- L1 cache reference 0.5 ns; mutex lock and unlock 25 ns; read 4 KB randomly
  from SSD 150 us; read 1 MB from a 1 Gbps network 10 ms.
- 1 Gbps Ethernet reads at 100 MB/s; 6 to 7 world-wide round trips per
  second; 2,000 round trips per second within a data center.
