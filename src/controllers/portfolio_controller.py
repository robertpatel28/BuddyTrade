#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the Portfolio class.
#

from models.portfolio import Portfolio
from services.db_service import DatabaseService
import yfinance as yf
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pandas_ta as ta
import pandas as pd




class PortfolioController:

    # Contructor for the portfolio controller.
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    # Creates a new portfolio.
    def create_portfolio(self, user_id: int) -> bool:
        try:
            conn = self.db_service.connect()
            # Creates cursor to push queries to db.
            cursor = conn.cursor()
            # Executes query to db.
            cursor.execute("""
                        INSERT INTO Portfolios (user_id) VALUES (?)
            """, (user_id,))
            conn.commit()
            # Closes connection to db and returns True for successful portfolio creation.
            cursor.close()
            conn.close()
            return True
        # Catches exceptions and returns False for failed portfolio creation.
        except Exception as e:
            print(e)
            return False
        
    # Exports a user's portfolio as a file.
    def export_portfolio(self, user_id: int) -> bool:
        # IN PROGRESS
        pass

    # Retrieves a portfolio given the user_id.
    def get_portfolio_by_user_id(self, user_id: int) -> Portfolio | None:
        try:
            conn = self.db_service.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Portfolios WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                portfolio_id = row
                return Portfolio(portfolio_id, user_id)
            return None
        except Exception as e:
            print(e)
            return None
        
    # Retrieves current price for a ticker.
    def get_current_price(self, ticker: str) -> float:
        __ticker__ = yf.Ticker(ticker)
        live_price = __ticker__.info["regularMarketPrice"]
        return live_price
    
    # Returns Yes/No for golden cross opportunity.
    def get_golden_cross(self, ticker: str) -> str:
        
        # Retrieves price data for ticker.
        price_data = yf.download(ticker, period="3mo", interval="1h", auto_adjust=True)
        
        # Calculate SMAs
        price_data['SMA_50'] = ta.sma(price_data['Close'], length=50)
        price_data['SMA_100'] = ta.sma(price_data['Close'], length=100)
        price_data['SMA_200'] = ta.sma(price_data['Close'], length=200)

        # Detect Golden Cross: yesterday SMA50 < SMA200 and today SMA50 > SMA200
        price_data['Golden_Cross'] = (
            (price_data['SMA_50'].shift(1) < price_data['SMA_200'].shift(1)) &
            (price_data['SMA_50'] > price_data['SMA_200'])
        )
        # Return result
        if price_data['Golden_Cross'].tail(5).any():
            result = 'Yes'
        else:
            result = 'No'
        return result

    # Retrieves the EMA for given dataframe.
    def get_ema(self, price_data: pd.DataFrame, leng: int):
        # Fetches the EMA
        price_data[f'EMA_{leng}'] = ta.ema(price_data['Close'], length=leng)
        # Retrieves the last piece of data which contains the EMA.
        latest_ema = price_data[f'EMA_{leng}'].dropna().iloc[-1]
        # Returns the EMA.
        return latest_ema

    # Retrieves the SMA for given dataframe.
    def get_sma(self, price_data: pd.DataFrame, leng: int):
        # Fetches the 50 day SMA
        price_data[f'SMA_{leng}'] = ta.sma(price_data['Close'], length=leng)
        # Retrieves the last piece of data which contains the SMA.
        latest_sma = price_data[f'SMA_{leng}'].dropna().iloc[-1]
        # Returns the SMA.
        return latest_sma

    # Retrieves the ADX for a given ticker.
    def get_adx(self, price_data: pd.DataFrame):
        length = 14
        lensig = 10

        adx_data = ta.adx(
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close'],
            length=length,
            lensig=lensig
        )

        adx_col = f'ADX_{lensig}'  # e.g., ADX_10

        if adx_col not in adx_data.columns:
            print(f"[ERROR] Column '{adx_col}' not found in ADX data: {adx_data.columns}")
            return None

        price_data['ADX'] = adx_data[adx_col]
        latest_adx = price_data['ADX'].dropna().iloc[-1]
        return latest_adx

    # Retrieves the RSI for a given ticker.
    def get_rsi(self, price_data: pd.DataFrame):
        # Fetches the RSI
        price_data['RSI'] = ta.rsi(price_data['Close'], length=14)
        # Retrieves the last piece of data which contains the RSI
        latest_rsi = price_data['RSI'].dropna().iloc[-1]
        # Returns the RSI
        return latest_rsi

    # Retrieves RSI Volume for a given ticker.
    def get_rsi_volume(self, price_data: pd.DataFrame):
        # Fetches the RSI Volume
        price_data['RSI_Volume'] = ta.rsi(price_data['Volume'], length=14)
        # Retrieves the last piece of data which contains the RSI Volume
        latest_rsi_volume = price_data['RSI_Volume'].dropna().iloc[-1]
        # Returns the rsi_volume
        return latest_rsi_volume
        
    # Helper method to fetch price_data for given ticker.
    def get_price_data(self, ticker: str):
        ticker = ticker.strip().upper()
        price_data = yf.download(ticker, period="3mo", interval="1h", auto_adjust=True)

        if price_data.empty or len(price_data) < 15:
            print(f"[ERROR] Insufficient or empty data for ticker '{ticker}'. Data rows: {len(price_data)}")
            return None

        # Flatten MultiIndex if needed
        if isinstance(price_data.columns, pd.MultiIndex):
            price_data.columns = price_data.columns.get_level_values(0)
        
        return price_data
    
