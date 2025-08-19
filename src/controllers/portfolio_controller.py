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
from datetime import datetime




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
    
    # Retrieves the market cap for given ticker.
    def get_market_cap(self, ticker: str) -> float | None:
        try:
            ticker_obj = yf.Ticker(ticker.strip().upper())
            market_cap = ticker_obj.info.get("marketCap")
            if market_cap is None:
                raise ValueError("Market cap not available for this ticker.")
            return market_cap
        except Exception:
            raise ValueError("Invalid ticker or data unavailable.") 
        
    # Returns the p/e ratio for given ticker.
    def get_pe_ratio(self, ticker: str) -> float | None:
        try:
            ticker_obj = yf.Ticker(ticker.strip().upper())
            pe_ratio = ticker_obj.info.get("trailingPE")
            if pe_ratio is None:
                raise ValueError("P/E ratio not available for this ticker.")
            return pe_ratio
        except Exception:
            raise ValueError("Invalid ticker or data unavailable.")
        
    # Returns the dividend yield for given ticker.
    def get_dividend_yield(self, ticker: str) -> str:
        try:
            ticker = ticker.strip().upper()
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info

            current_price = info.get("currentPrice")
            trailing_dividend = info.get("trailingAnnualDividendRate")

            if current_price and trailing_dividend:
                dividend_yield = (trailing_dividend / current_price) * 100
                if 0 < dividend_yield <= 20:  # realistic range
                    return f"{dividend_yield:.2f}%"

            # Fallback to Yahoo's dividendYield if primary fails
            raw_yield = info.get("dividendYield")
            if isinstance(raw_yield, (int, float)) and 0 < raw_yield <= 0.2:  # 0.2 = 20%
                return f"{raw_yield * 100:.2f}%"

            return "N/A"

        except Exception:
            return "N/A"

    # Returns the earnings per share for given ticker.
    def get_eps(self, ticker: str) -> float | None:
        try:
            ticker_obj = yf.Ticker(ticker.strip().upper())
            eps = ticker_obj.info.get("trailingEps")  # or "forwardEps"
            return eps
        except Exception:
            raise ValueError("Invalid ticker or EPS unavailable.")
                
    # Retrieves current time.
    def get_datetime(self) -> str:
        current_time_str = datetime.now().strftime("%H:%M:%S")
        return current_time_str
    
    # Returns true if a golden_cross is present, false otherwise.
    def is_golden_cross(self, ticker: str, price_data: pd.DataFrame) -> bool:
        sma50 = price_data["Close"].rolling(50).mean()
        sma200 = price_data["Close"].rolling(200).mean()
        if pd.isna(sma50.iloc[-1]) or pd.isna(sma200.iloc[-1]):
            return False
        return sma50.iloc[-1] > sma200.iloc[-1]

    
    # Returns short-term momentum signal: "Bullish", "Bearish", or "Neutral"
    def get_short_momentum(self, price_data: pd.DataFrame) -> str:
        if price_data is None or price_data.empty:
            return "N/A"
        if "Close" not in price_data.columns:
            return "N/A"
        if len(price_data) < 20:  # not enough for short EMAs
            return "N/A"

        ema_10 = price_data["Close"].ewm(span=10, adjust=False).mean()
        ema_20 = price_data["Close"].ewm(span=20, adjust=False).mean()

        # Compare latest values
        if ema_10.iloc[-1] > ema_20.iloc[-1]:
            return "Bullish"
        elif ema_10.iloc[-1] < ema_20.iloc[-1]:
            return "Bearish"
        else:
            return "Neutral"
        
    # Returns True if the current price is above the 200 EMA, False otherwise
    def is_price_over_200_ema(self, price_data: pd.DataFrame) -> bool:
        latest_ema_200 = self.get_ema(price_data, 200)
        if latest_ema_200 is None:
            return False
        latest_close = price_data["Close"].iloc[-1]
        return latest_close > latest_ema_200

    # Returns True if RSI is strong, False otherwise.
    def get_rsi_strength(self, price_data: pd.DataFrame, threshold: float = 70) -> bool:
        latest_rsi = self.get_rsi(price_data)
        if latest_rsi is None:
            return False
        return latest_rsi >= threshold

    # Returns True is RSI is oversold, False otherise.
    def is_rsi_oversold(self, price_data: pd.DataFrame, threshold: float = 30) -> bool:
        latest_rsi = self.get_rsi(price_data)
        if latest_rsi is None:
            return False
        return latest_rsi <= threshold

    # Returns True if ADX is above 25 (strong trend)
    def is_adx_strong(self, price_data: pd.DataFrame) -> bool:
        latest_adx = self.get_adx(price_data)
        if latest_adx is None:
            return False
        return latest_adx > 25
    
    # Detects if current price is in a pullback during an uptrend
    def pullback_opportunity(self, ticker: str, price_data: pd.DataFrame) -> bool:
        if price_data is None or price_data.empty:
            return False

        current_price = self.get_current_price(ticker)
        ema_200 = self.get_ema(price_data, 200)
        rsi = self.get_rsi(price_data)

        if ema_200 is None or rsi is None:
            return False

        # In uptrend AND RSI in pullback range
        return current_price > ema_200 and 40 <= rsi <= 50
    
    # Detects if current volume is significantly higher than recent average
    def volume_spike(self, price_data: pd.DataFrame, multiplier: float = 1.5) -> bool:
        if price_data is None or price_data.empty:
            return False
        if "Volume" not in price_data.columns:
            return False
        if len(price_data) < 20:  # need enough data for average
            return False

        avg_volume = price_data["Volume"].rolling(20).mean().iloc[-1]
        current_volume = price_data["Volume"].iloc[-1]

        if pd.isna(avg_volume) or pd.isna(current_volume):
            return False

        return current_volume > avg_volume * multiplier
    
    # Checks if the current volume is in the top X% of the last N periods
    def high_volume(self, price_data: pd.DataFrame, percentile: float = 0.9) -> bool:
        if price_data is None or price_data.empty:
            return False
        if "Volume" not in price_data.columns:
            return False
        if len(price_data) < 20:
            return False

        # Get volume threshold at the given percentile
        threshold = price_data["Volume"].quantile(percentile)
        current_volume = price_data["Volume"].iloc[-1]

        if pd.isna(threshold) or pd.isna(current_volume):
            return False

        return current_volume >= threshold

    # Helper method to fetch price_data for given ticker.
    def get_price_data(self, ticker: str):
        ticker = ticker.strip().upper()
        price_data = yf.download(ticker, period="3mo", interval="1h", auto_adjust=True)

        if price_data.empty or len(price_data) < 15:
            raise ValueError("No price data found.")

        # Flatten MultiIndex if needed
        if isinstance(price_data.columns, pd.MultiIndex):
            price_data.columns = price_data.columns.get_level_values(0)
        
        return price_data

