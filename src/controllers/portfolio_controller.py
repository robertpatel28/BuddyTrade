#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the Portfolio class.
#

from models.portfolio import Portfolio
from services.db_service import DatabaseService

class Portfolio:

    # Database instantiated and assigned to variable.
    db_service = DatabaseService()

    # Portfolio instantiated and assigned to variable.
    portfolio = Portfolio()

    # Constructs a new Portfolio instance.
    def __init__(self):
        self.portfolios = {}

    # Creates a new portfolio.
    def create_portfolio(self):
        pass
