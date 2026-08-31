CREATE TABLE securities IF NOT EXISTS (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    ticker TEXT NOT NULL UNIQUE,
    company_name TEXT,
    market_cap INTEGER,
    pe_ratio DOUBLE,
    exchange TEXT,
    date DATE,
    screening_status TEXT
);

CREATE TABLE sectors IF NOT EXISTS (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    sector_name TEXT NOT NULL UNIQUE
);

CREATE TABLE security_x_sector IF NOT EXISTS(
    security_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    PRIMARY KEY (security_id, sector_id)
    FOREIGN KEY (security_id) REFERENCES securities(id) ON DELETE CASCADE,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE
);