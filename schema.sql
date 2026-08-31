CREATE TABLE securities IF NOT EXISTS (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    ticker TEXT NOT NULL UNIQUE,
    company_name TEXT,
    market_cap INTEGER,
    pe_ratio DOUBLE,
    exchange TEXT,
    date DATE
);