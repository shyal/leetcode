REFERENCE: d229 TCP Or UDP
SOURCE: System Design Primer, "Transmission control protocol (TCP)" and "User datagram protocol (UDP)" https://github.com/donnemartin/system-design-primer#transmission-control-protocol-tcp

REQUIRED
- TCP is connection-oriented, set up and torn down with a handshake; all
  packets sent are guaranteed to reach the destination in the original order
  and without corruption.
- Two mechanisms out of: sequence numbers and checksum fields on each
  packet; the sender resends when it gets no correct response; flow control;
  congestion control.
- UDP is connectionless: datagrams may reach their destination out of order
  or not at all, and there is no congestion control. Without those
  guarantees it is generally more efficient.
- Choose TCP when you need all of the data to arrive intact, and when you
  want an automatic best estimate use of the network throughput.
- Choose UDP when you need the lowest latency, when late data is worse than
  lost data, and when you want to implement your own error correction.
- TCP: web servers, database traffic, SMTP, FTP, SSH. UDP: VoIP, video chat,
  streaming, realtime multiplayer games.

ALSO TRUE
- Many open TCP connections cost memory; connection pooling helps.
- UDP can broadcast to every device on the subnet, which DHCP relies on.
