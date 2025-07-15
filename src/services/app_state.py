#
# Author: Robert Patel
# Manages the state of the user within the application.
#

from models.user import User
from models.portfolio import Portfolio

class AppState():


    def __init__(self):
        self.current_user = None
        self.current_portfolio = None
        self.is_authenticated = False

    # Sets current_user
    def set_current_user(self, user: User):
        self.current_user = user
        self.is_authenticated = user.is_user_authenticated()

    # Gets the current_user
    def get_current_user(self) -> User:
        return self.current_user
    
    # Sets the current_portfolio
    def set_current_portfolio(self, portfolio: Portfolio):
        self.current_portfolio = portfolio

    # Gets the current_portfolio
    def get_current_portfolio(self) -> Portfolio:
        return self.current_portfolio
    
    # Gets is_authenticated
    def is_user_authenticated(self) -> bool:
        return self.is_authenticated
    
    # Resets application for logged-out user.
    def logout(self):
        self.current_user = None
        self.current_portfolio = None
        self.is_authenticated = False