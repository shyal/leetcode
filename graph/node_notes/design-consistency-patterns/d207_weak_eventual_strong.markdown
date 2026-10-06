REFERENCE: d207 Weak Eventual Strong
SOURCE: System Design Primer, "Consistency patterns" https://github.com/donnemartin/system-design-primer#consistency-patterns

REQUIRED
- Weak: after a write, reads may or may not see it; best effort. Seen in
  memcached; suits VoIP, video chat and realtime multiplayer games.
- Eventual: after a write, reads will eventually see it, typically within
  milliseconds; data is replicated asynchronously. Seen in DNS and email;
  suits highly available systems.
- Strong: after a write, reads will see it; data is replicated
  synchronously. Seen in file systems and RDBMSes; suits systems that need
  transactions.

ALSO TRUE
- On a phone call that loses reception for a few seconds, what was said in
  the gap is never heard: that is weak consistency.
