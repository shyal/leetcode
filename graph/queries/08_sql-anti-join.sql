-- QUERY: Never Touched
-- TRAINS: sql-anti-join
--
-- Tables:
--
--     nodes
--         id     TEXT
--         name   TEXT
--         group  TEXT
--         added  TEXT
--         desc   TEXT
--         hint   TEXT
--         drill  TEXT
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
-- Return every node that has no verdict at all.
-- Columns: node_id.
--
-- REQUIRED: NOT EXISTS or a LEFT JOIN ... IS NULL. NOT IN over a column that
-- can be NULL is the failure mode this kills.

select n.id
    from nodes as n
    left join verdicts as v on v.node_id = n.id
    where v.node_id is null;