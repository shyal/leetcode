-- QUERY: Problems Without A Source
-- TRAINS: sql-null-semantics
--
-- Tables:
--
--     problems
--         num         TEXT
--         title       TEXT
--         difficulty  TEXT
--         source      TEXT
--         note        TEXT
--         banned      INTEGER
--
-- Return every problem whose source is anything other than 'extracted',
-- including problems that have no source at all, ordered by number.
-- Columns: num, title, source.
--
-- REQUIRED: the count must include the NULL rows. `source != 'extracted'`
-- alone is the failure mode this query exists to kill.

select num, title, source
    from problems
    where (source is not 'extracted' or source is null)
    order by num;