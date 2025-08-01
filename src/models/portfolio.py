#
# Author: Robert Patel
# Portfolio class which contains getters/setters for Portfolio object.
#

from models.holding import Holding
from services.db_service import DatabaseService


class Portfolio:

    # Contstructs a new Portfolio
    def __init__(self, portfolio_id: int, db_service: DatabaseService, holdings=None):
        self.portfolio_id = portfolio_id
        self.db_service = db_service
        self.holdings = holdings if holdings is not None else {}
    
    # Gets the portfolio_id
    def get_portfolio_id(self) -> int:
        return self.portfolio_id

    # Gets a list of the holdings in the portfolio
    def get_all_holdings(self) -> list:
        return list(self.holdings.values())
    
    # Sets the list of holdings in the portfolio
    def get_holding(self, ticker: str) -> Holding | None:
        return self.holdings.get(ticker)
    
    # Removes a holding from the portfolio
    def remove_holding(self, ticker: str) -> bool:
        if ticker in self.holdings:
            del self.holdings[ticker]
            return True
        else:
            return False

    # Calculate total value of the portfolio
    def calculate_total_value(self) -> float:
        return sum(holding.get_quantity() * holding.get_price_per_share() for holding in self.holdings.values())
    
    # Calculate total gain / loss of the portfolio
    def calculate_gain_or_loss(self) -> float:
        return sum(holding.calculate_gain_or_loss() for holding in self.holdings.values())