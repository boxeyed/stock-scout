# Similar shape to lab scout, reassess need for changes after basic handling completed.
# Moved to .py file to avoid complications with file paths.
# Usage: import where a fresh database must be setup and execute the schema script.

SCHEMA = '''
CREATE TABLE IF NOT EXISTS securities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE,
    company_name TEXT,
    exchange TEXT,
    current_price DOUBLE,
    screening_status TEXT DEFAULT "Watching",
    market_cap INTEGER,
    last_updated DATE
);

CREATE TABLE IF NOT EXISTS sectors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS security_x_sector(
    security_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    PRIMARY KEY (security_id, sector_id)
    FOREIGN KEY (security_id) REFERENCES securities(id) ON DELETE CASCADE,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE
);'''