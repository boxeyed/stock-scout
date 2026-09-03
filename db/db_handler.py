import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime, timezone
from schema import SCHEMA

DATABASE = "scout.db"
WATCHLIST = "csv/watchlist.csv"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def setup_db(connection: sqlite3.Connection):
  """Establish connection to DB and setup"""
  connection.executescript(SCHEMA)
  connection.commit()

def display_db(connection: sqlite3.Connection):
  """Display DB values through console"""
  df = pd.read_sql_query("SELECT * FROM securities")
  print(df)

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
        current_price: float = float(row["Current Price"]) if pd.notna(row["Current Price"]) else None
        screening_status: str = row["Screening Status"] if pd.notna(row["Screening Status"]) else "Watching"
        market_cap: float = float(row["Market Cap"]) if "Market Cap" in row and pd.notna(row["Market Cap"]) else None
        last_updated = row["Last Updated"] if "Last Updated" in row and pd.notna(row["Last Updated"]) else None

        cursor: sqlite3.Cursor = connection.execute("INSERT INTO securities (ticker, company_name, exchange, current_price, screening_status, market_cap, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)",(ticker, company_name, exchange, current_price, screening_status, market_cap, last_updated))
        security_id = cursor.lastrowid

        # to 'sectors' table
        for sector in row["Sectors"].split(","):
            sector: str = sector.strip()
            if sector not in sectors:                       
                cursor = connection.execute("INSERT INTO sectors (sector_name) VALUES (?)", (sector,)) 
                sectors[sector] = cursor.lastrowid

        # to 'security_x_sector' table
            connection.execute("INSERT INTO security_x_sector (security_id, sector_id) VALUES (?, ?)", (security_id, sectors[sector]))
            inserted = inserted + 1

   connection.commit()
   return inserted

def refresh_watchlist(connection: sqlite3.Connection):
   """Pull data from yfinance to populate current_price, market_cap, last_updated for each ticker in watchlist."""
   refreshed = 0

   watchlist_df = pd.read_csv(WATCHLIST)

   for index, row in watchlist_df.iterrows():
      # Get ticker object to pull corresponding data from yfinance
      ticker = yf.Ticker((row["Ticker"]))

      # pull data according to yfinance
      market_cap = ticker.info.get("marketCap")
      current_price = ticker.info.get("currentPrice")

      # get last updated (time)
      last_updated =  "" + str(datetime.now(timezone.utc)) + " " + str(datetime.now(timezone.utc).tzname())

      # edit the watchlist.csv's corresponding values
      watchlist_df.at[index, "Market Cap"] = market_cap
      watchlist_df.at[index, "Current Price"] = current_price
      watchlist_df.at[index, "Last Updated"] = last_updated

      refreshed+=1

   watchlist_df.to_csv()
   return refreshed 




      

def main():
  connection = get_connection()
  setup_db(connection)
  refresh_watchlist(connection)
  migrate_watchlist(connection)
  
if __name__ == "__main__":
    main()