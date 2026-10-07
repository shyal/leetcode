REFERENCE: d256 Twitter Fan Out Bottleneck
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- Bottleneck: the Fan Out Service. A user with millions of followers takes
  minutes to fan out, which can race with replies; re-order the tweets at
  serve time.
- Or do not fan out the tweets of highly-followed users: search for their
  tweets, merge the results with the home timeline, and re-order at serve
  time.
