import yfinance as yf
import sqlite3
import pandas as pd
import db.db_handler

def display_db(connection: sqlite3.Connection):
  """Display DB values through console"""
  df = pd.read_sql_query("SELECT * FROM securities", connection)
  print(df)