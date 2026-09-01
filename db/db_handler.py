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
     cursor.executescript(p.read)

  connection.commit()

def display_db():
  """Display DB values through console"""
  return 0

def migrate_watchlist(connection: sqlite3.Connection):
   """Migrate data from values in watchlist (csv) to the DB"""

   df = pd.read_csv(WATCHLIST)
   inserted = 0 # keeps track of count of inserted data vals

   existing_tickers = {row["ticker"] for row in connection.execute("SELECT ticker FROM securities")}

   for _, row in df.iterrows():

        # to 'securities' table
        ticker: str = row["Ticker"]
        if ticker in existing_tickers:  # checks the data is not already in db
            continue
        
        company_name: str = row["Company Name"]
        exchange: str = row["Exchange"]
        current_price: float = row["Current Price"]
        screening_status: str = row["Screening Status"]
        market_cap: float = row["Market Cap"]
        last_updated = row["Last Updated"]

        



def main():
  print("Hello world")
  
if __name__ == "__main__":
    main()