import yfinance as yf
import sqlite3
import pandas as pd
import numpy as np

DATABASE = "scout.db"
WATCHLIST = "watchlist.csv"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def setup_db():
  """Establish connection to DB and setup"""
  return 0

def display_db():
  """Display DB values through console"""
  return 0

def migrate_watchlist():
   """Migrate data from values in watchlist to the DB"""
   return 0

def main():
  print("Hello world")
  
if __name__ == "__main__":
    main()