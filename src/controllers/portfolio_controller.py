#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the Portfolio class.
#

from models.portfolio import Portfolio
from services.db_service import DatabaseService

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
        
    
    