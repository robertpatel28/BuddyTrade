#
# Author: Robert Patel
# This class is utilized to manage API services within the application.
#

import yfinance as yf

# Class that handles API services and operations.
class APIService:

    # Retrieve the current price of a passed-in ticker.
    def get_current_price(self, ticker: str) -> float:
        pass

    # Fetches price data of a passed-in ticker.
    def get_historical_data(self, ticker: str, period: str) -> list[float]:
        pass

    # Fetches company information (name, sector, industry).
    def get_company_information(self, ticker: str) -> dict:
        pass

    # Returns list of relevant market news articles.
    def get_market_news(self) -> list[dict]:
        pass

    # Retrieves the price-to-earnings ratio.
    def get_pe_ratio(self, ticker: str) -> float:
        pass

    # Retrieves the dividend yield for a given stock.
    def get_dividend_yield(self, ticker: str) -> float:
        pass

    # Validates if a ticker is linked to a stock listed on the market.
    def validate_ticker(self, ticker: str) -> bool:
        pass

    # Retrieves SMA for stock with given interval.
    def get_sma(self, ticker: str, interval: str) -> float:
        pass

    # Retrieves EMA for stock with given interval.
    def get_ema(self, ticker: str, interval: str) -> float:
        pass

    # Retrieves ADX for stock with given period.
    def get_adx(self, ticker: str, period: int) -> float:
        pass

    # Retrieves RSI for stock with given period.
    def get_rsi(self, ticker: str, period: int) -> float:
        pass

    
