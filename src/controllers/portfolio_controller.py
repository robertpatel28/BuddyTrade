#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the Portfolio class.
#

from models.portfolio import Portfolio
from services.db_service import DatabaseService

class PortfolioController:

    # Contructor for the portfolio controller.
    def __init__(self, db_service: DatabaseService, current_portfolio: Portfolio | None = None):
        self.db_service = db_service
        self.curret_portfolio = current_portfolio

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
    