-- PRAGMA sql_trace = ON;

-- SELECT * FROM CUST;

-- SELECT * FROM query_history ORDER BY executed_at DESC;

CREATE TABLE IF NOT EXISTS query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    executed_at TEXT
);

CREATE TRIGGER log_insert_trigger
AFTER INSERT ON CUST
BEGIN
    INSERT INTO query_history (query, executed_at)
    VALUES ('INSERT INTO CUST VALUES(...)', DATETIME('now'));
END;


CREATE TABLE IF NOT EXISTS query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    execution_count INTEGER,
    total_time REAL,
    average_time REAL,
    rows_processed INTEGER,
    disk_io INTEGER,
    cache_hits INTEGER,
    start_time TIMESTAMP,
    end
