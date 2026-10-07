REFERENCE: d265 Mint Category
SOURCE: System Design Primer, "Design Mint.com" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md

REQUIRED
- Category: a seller-to-category dictionary seeded with the most popular
  sellers. 50,000 sellers at under 255 bytes each is about 12 MB of memory.
  Sellers not seeded are learned from the users' manual overrides.
