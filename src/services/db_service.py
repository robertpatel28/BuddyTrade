#
# Author: Robert Patel
# This class connects the application to the Database
# and handles interactions between the Database and the
# application.
#

import sys
import os
import pyodbc
from datetime import datetime
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
            print("✅ Database connection successful.")
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
    def get_user_portfolio(self, user_id: str) -> list[dict] | None:
        
        # Connects to db.
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT
                    ticker,
                    entry_price,
                    shares_owned,
                    current_price,
                    gain_loss,
                    recommendation
                FROM
                    Portfolios
                WHERE
                    user_id = ?
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            # Convert to list of dicts
            portfolio = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(e)
        finally:
            conn.close()

    # Saves a holding currently in a portfolio in the database.
    def save_holding(self, ticker: str, quantity: int, price: float) -> bool | None:
        # Connects to db
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            cursor = self.conn.cursor()
            query = ("UPATE holdings SET ticker = ?, quantity = ?, price = ? ", (ticker, quantity, price,))
            cursor.execute(query)
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
    def add_holding(self, ticker: str, purchase_price: float, quantity: int, date_time: datetime):
        # Connects to db
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            cursor = self.conn.cursor()
            query = ("INSERT INTO Holdings (portfolio_id, ticker, buy_price, quantity, date_added)VALUES (?, ?, ?, ?, ?)")
            cursor.execute(query)
        except Exception as e:
            print(e)
        finally:
            conn.close()