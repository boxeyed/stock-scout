import yfinance as yf
import sqlite3
import pandas as pd
import data.db_handler as dbh


def refresh_db(connection: sqlite3.Connection):
  return 0

def add_security_manual(connection: sqlite3.Connection):
  return 0

def add_security_auto(connection: sqlite3.Connection):
  return 0

def scout_securities(connection: sqlite3.Connection):
  return 0

def main():
  con = dbh.get_connection()
  dbh.setup_db(con)