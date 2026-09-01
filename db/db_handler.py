import yfinance as yf
import sqlite3
import pandas as pd
import numpy as np

DATABASE = "scout.db"
WATCHLIST = "watchlist.csv"
SCHEMA = "schema.sql"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def setup_db(connection: sqlite3.Connection):
  """Establish connection to DB and setup"""
  cursor = connection.cursor()

  with open(SCHEMA) as p:
     cursor.executescript(p.read())

  connection.commit()

def display_db():
  """Display DB values through console"""
  return 0

def migrate_watchlist(connection: sqlite3.Connection):
   """Migrate data from values in watchlist (csv) to the DB"""

   df = pd.read_csv(WATCHLIST)
   inserted = 0 # keeps track of count of inserted data vals

   existing_tickers = {row["ticker"] for row in connection.execute("SELECT ticker FROM securities")}
   sectors = {row["sector_name"] : row["id"] for row in connection.execute("SELECT sector_name, id FROM sectors")} 

   for _, row in df.iterrows():

        # to 'securities' table
        ticker = row["Ticker"].strip().upper() if pd.notna(row["Ticker"]) else None
        if ticker is None:              # ensures ticker is a mandatiry field
           print("Skipping row--blank ticker...")
           continue
        if ticker in existing_tickers:  # checks the data is not already in db
            continue
        
        company_name: str = row["Company Name"] if pd.notna(row["Company Name"]) else "Unknown"
        exchange: str = row["Exchange"] if pd.notna(row["Exchange"]) else "Unknown"
        latest_price: float = float(row["Latest Price"]) if pd.notna(row["Latest Price"]) else None
        screening_status: str = row["Screening Status"] if pd.notna(row["Screening Status"]) else "Watching"
        market_cap: float = float(row["Market Cap"]) if "Market Cap" in row and pd.notna(row["Market Cap"]) else None
        last_updated = row["Last Updated"] if "Last Updated" in row and pd.notna(row["Last Updated"]) else None

        cursor: sqlite3.Cursor = connection.execute("INSERT INTO securities (ticker, company_name, exchange, latest_price, screening_status, market_cap, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)",(ticker, company_name, exchange, latest_price, screening_status, market_cap, last_updated))
        security_id = cursor.lastrowid

        # to 'sectors' table
        for sector in row["Sectors"].split(","):
            sector: str = sector.strip()
            if sector not in sectors:                       
                cursor = connection.execute("INSERT INTO sectors (sector_name) VALUES (?)", (sector,)) 
                sectors[sector] = cursor.lastrowid

        # to 'security_x_sector' table
            connection.execute("INSERT INTO security_x_sectors (security_id, sector_id) VALUES (?, ?)", (security_id, sectors[sector]))
            inserted = inserted + 1


   connection.commit()
   return inserted




        





def main():
  print("Hello world")
  
if __name__ == "__main__":
    main()