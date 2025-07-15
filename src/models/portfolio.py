#
# Author: Robert Patel
# Portfolio class which contains getters/setters for Portfolio object.
#
from models.holding import Holding


class Portfolio:

    # Contstructs a new Portfolio
    def __init__(self, portfolio_id: int, user_id: int, name: str, holdings=None):
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.name = name
        self.holdings = holdings if holdings is not None else {}
    
    # Gets the portfolio_id
    def get_portfolio_id(self):
        return self.portfolio_id
    
    # Sets the portfolio_id
    def set_portfolio_id(self, portfolio_id: int):
        self.portfolio_id = portfolio_id

    # Gets the user_id
    def get_user_id(self) -> int:
        return self.user_id
    
    # Sets the user_id
    def set_user_id(self, user_id: int):
        self.user_id = user_id

    # Gets the name of the portfolio
    def get_name(self) -> str:
        return self.name
    
    # Sets the name of the portfolio
    def set_name(self, name: str):
        self.name = name

    # Gets a list of the holdings in the portfolio
    def get_all_holdings(self) -> list:
        return list(self.holdings.values())
    
    # Sets the list of holdings in the portfolio
    def get_holding(self, ticker: str) -> str:
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
        return sum(holding.get * holding.price_per_share for holding in self.holdings.values())
    
    # Calculate total gain / loss of the portfolio
    def calculate_gain_or_loss(self) -> float:
        return sum(holding.calculate_gain_or_loss() for holding in self.holdings.values())