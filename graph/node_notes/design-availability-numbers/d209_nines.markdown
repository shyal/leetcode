REFERENCE: d209 Nines
SOURCE: System Design Primer, "Availability in numbers" https://github.com/donnemartin/system-design-primer#availability-in-numbers

REQUIRED
- 99.9%, three 9s: 8 hours 45 minutes 57 seconds of downtime per year.
- 99.99%, four 9s: 52 minutes 36 seconds of downtime per year.
- In sequence: total = A * B. Two components at 99.9% give 99.8%, lower than
  either.
- In parallel: total = 1 - (1 - A) * (1 - B). Two components at 99.9% give
  99.9999%, higher than either.

ALSO TRUE
- 99.9% is 43 minutes 50 seconds per month and 1 minute 26 seconds per day;
  99.99% is 4 minutes 23 seconds per month and 8.6 seconds per day.
