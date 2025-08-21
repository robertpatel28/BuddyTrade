#
# Author: Robert Patel
# This class connects the application to the Database
# and handles interactions between the Database and the
# application.
#

import sys
import os
import pyodbc
import yfinance as yf
from datetime import datetime
from collections import defaultdict
from models.user import User
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER

# Handles interactions between the database and the application.
class DatabaseService:

    # Connects to the database
    def connect(self):
        connection_string = (
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )

        try:
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            print("❌ Connection failed:", e)
            return None

    # Retrieves a user via email search.
    def get_user_by_email(self, email: str) -> User | None:
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, last_name, hashed_password, email FROM Users WHERE email = ?", (email,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                # row = (first_name, last_name, hashed_password, email)
                return User(first_name=row[0], last_name=row[1], hashed_password=row[2], email=row[3])
            return None
        except Exception as e:
            print(f"❌ Error retrieving user: {e}")
            return None
        
    # Retrieves the user ID using the email to search.
    def get_user_id(self, email: str) -> int | None:
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                return row[0]
            else:
                return None
            
        except Exception as e:
            print(e)
            return None

    def get_portfolio_id(self, user_id: int) -> int | None:
        # Connects to db and fetches the portfolio_id linked with the given user_id.
        try:
            # Connects to db and creates cursor to execute query.
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Portfolios WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            # Closes the connections to the db.
            cursor.close()
            conn.close()
            return row[0] if row else None
        except Exception as e:
            print("Error retrieving portfolio ID:", e)
            return None

    # Verifies the existence of an email in the database.
    def email_exists(self, email: str) -> bool:
        if self.get_user_by_email(email):
            return True
        else:
            return False

    # Retrieves a user's portfolio from the database.
    def get_user_portfolio(self, portfolio_id: int) -> list[dict] | None:
        
        # Connects to db.
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT
                    ticker,
                    buy_price,
                    quantity,
                    date_added
                FROM
                    Holdings
                WHERE
                    portfolio_id = ?
            """
            cursor.execute(query, (portfolio_id))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            # Convert to list of dicts
            portfolio = [dict(zip(columns, row)) for row in rows]
            return portfolio
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

    # Saves a holding currently in a portfolio in the database.
    def save_holding(self, ticker: str, quantity: int, price: float, datetime: datetime) -> bool | None:
        # Connects to db
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            query = ("UPATE holdings SET ticker = ?, quantity = ?, price = ? ")
            cursor.execute(query, (ticker, quantity, price, datetime))
        except Exception as e:
            print(e)
        finally:
            conn.close( )

    # Remove's a holding from a portfolio in the database.
    def remove_holding(self, user_id: int, ticker: str) -> bool:
        pass

    # Retrieves a watchlist from the database.
    def get_watchlist(self, user_id: int) -> list[str]:
        pass

    # Adds a ticker to a watchlist in the database.
    def add_to_watchlist(self, user_id: int, ticker: str, color_id: int) -> bool:
        pass

    # Removes a ticker from the watchlist in the database.
    def remove_from_watchlist(self, user_id: int, ticker: str, color_id: int) -> bool:
        pass

    # Adds a holding to the database into the 'Holdings' table.
    def add_holding(self, ticker: str, purchase_price: float, quantity: int, date_time: datetime, portfolio_id: int) -> bool:
        conn = self.connect()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            if isinstance(date_time, datetime):
                date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

            query = "INSERT INTO Holdings (portfolio_id, ticker, buy_price, quantity, date_added) VALUES (?, ?, ?, ?, ?)"

            cursor.execute(query, (portfolio_id, ticker, purchase_price, quantity, date_time))
            conn.commit()
            return True
        except Exception as e:
            print("❌ SQL Error:", e)
            return False
        finally:
            conn.close()

    def get_holding(self):
        return
    
    # Retrieves {ticker: quantity} for a user's portfolio.
    def get_tickers(self, portfolio_id: int) -> dict[str, int]:
        conn = self.connect()
        if conn is None:
            return {}

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT ticker, quantity
                FROM Holdings
                WHERE portfolio_id = ?
                """,
                (portfolio_id,),
            )
            rows = cursor.fetchall()

            tickers: dict[str, int] = {}
            for r in rows:
                if not r or r[0] is None:
                    continue
                ticker = str(r[0]).upper()
                qty = int(r[1]) if r[1] is not None else 0
                tickers[ticker] = tickers.get(ticker, 0) + qty  # aggregate if duplicates

            return tickers
        except Exception as e:
            print(e)
            return {}
        finally:
            conn.close()

    # Retrieves the total market value of the user's portfolio (sum of qty * current price).
    def get_portfolio_value(self, portfolio_id: int) -> float | None:
        conn = self.connect()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    ticker,
                    quantity
                FROM
                    Holdings
                WHERE
                    portfolio_id = ?
            """, (portfolio_id,))
            rows = cursor.fetchall()
            if not rows:
                return 0.0

            # Aggregate quantities per ticker in case of duplicates
            qty_by_ticker = defaultdict(float)
            for r in rows:
                tkr = (r[0] or "").upper().strip()
                qty = float(r[1] or 0)
                if tkr and qty > 0:
                    qty_by_ticker[tkr] += qty

            if not qty_by_ticker:
                return 0.0

            # Batch fetch using Tickers
            tickers_str = " ".join(qty_by_ticker.keys())
            ts = yf.Tickers(tickers_str)

            total = 0.0
            for tkr, qty in qty_by_ticker.items():
                t = ts.tickers[tkr]
                price = None

                # Fast path
                fi = getattr(t, "fast_info", None)
                if fi:
                    price = fi.get("last_price")

                # Fallbacks
                if price is None:
                    info = getattr(t, "info", {})
                    price = info.get("regularMarketPrice")

                if price is None:
                    hist = t.history(period="1d", interval="1m")
                    if not hist.empty:
                        price = float(hist["Close"].dropna().iloc[-1])

                if price is not None:
                    total += float(price) * qty
                # else: skip ticker with no price available

            return round(total, 2)
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

# Returns the portfolio's total profit (current value - cost basis).
    def get_portfolio_profit(self, portfolio_id: int) -> float | None:
        conn = self.connect()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    ticker,
                    quantity,
                    buy_price
                FROM
                    Holdings
                WHERE
                    portfolio_id = ?
            """, (portfolio_id,))
            rows = cursor.fetchall()
            if not rows:
                return 0.0

            # Sum cost basis across lots; also collect total qty per ticker for live pricing
            cost_basis = 0.0
            qty_by_ticker = defaultdict(float)
            for tkr, qty, buy_price in rows:
                if not tkr:
                    continue
                tkr = tkr.upper().strip()
                q = float(qty or 0)
                bp = float(buy_price or 0)
                if q <= 0:
                    continue
                cost_basis += q * bp
                qty_by_ticker[tkr] += q

            if not qty_by_ticker:
                return 0.0

            # Fetch current prices in one shot
            ts = yf.Tickers(" ".join(qty_by_ticker.keys()))
            current_value = 0.0
            for tkr, q in qty_by_ticker.items():
                t = ts.tickers[tkr]
                price = None

                fi = getattr(t, "fast_info", None)
                if fi:
                    price = fi.get("last_price")

                if price is None:
                    info = getattr(t, "info", {})
                    price = info.get("regularMarketPrice")

                if price is None:
                    hist = t.history(period="1d", interval="1m")
                    if not hist.empty:
                        price = float(hist["Close"].dropna().iloc[-1])

                if price is not None:
                    current_value += float(price) * q

            profit = current_value - cost_basis
            return round(profit, 2)
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

    # In your DatabaseService
    def get_avg_buy_price(self, portfolio_id: int, ticker: str) -> float | None:
        conn = self.connect()
        if conn is None:
            return None
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    CASE WHEN SUM(quantity) = 0 THEN NULL
                        ELSE SUM(quantity * buy_price) / SUM(quantity)
                    END AS avg_buy_price
                FROM Holdings
                WHERE portfolio_id = ? AND UPPER(ticker) = UPPER(?)
            """, (portfolio_id, ticker))
            row = cur.fetchone()
            return float(row[0]) if row and row[0] is not None else None
        finally:
            conn.close()
