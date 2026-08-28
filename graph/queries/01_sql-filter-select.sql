-- QUERY: Unbanned Hards
-- TRAINS: sql-filter-select
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
-- Return every problem that is Hard and not banned, ordered by number.
-- Columns: num, title.
--
-- REQUIRED: one SELECT with a WHERE and an ORDER BY. NO post-filtering by eye.

select num, title
    from problems
    where
        difficulty is 'Hard'
        and banned = 0
    order by num;