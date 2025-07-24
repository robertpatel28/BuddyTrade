#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the User class.
#

from models.user import User
from services.db_service import DatabaseService
from services.auth_service import AuthService
from services.app_state import AppState
from PyQt6.QtWidgets import QMainWindow
from controllers.screen_manager import ScreenManager
from controllers.portfolio_controller import PortfolioController

# Handles interactions regarding the User's information in the database.
class UserController:

    # Constructor for user_controller class.
    def __init__(self, current_user: User, auth_service: AuthService, db_service: DatabaseService, app_state: AppState, screen_manager: ScreenManager, portfolio_controller: PortfolioController):
        self.current_user = current_user
        self.auth_service = auth_service
        self.db_service = db_service
        self.app_state = app_state
        self.screen_manager = screen_manager
        self.portfolio_controller = portfolio_controller

    # Logins user into the application.
    def login_user(self, email: str, password: str) -> bool:
        conn = self.db_service.connect()
        # Validates the connection.
        if conn is None:
            return None

        # Retrieves the user email.
        user = self.db_service.get_user_by_email(email)

        if not user:
            raise ValueError("User not found in database.")
        if not self.auth_service.verify_password(password, user.get_hashed_password()):
            raise ValueError("Incorrect Password.")
        
        # User login successful, transitions to dashboard.
        user.set_authenticated_status(True)
        self.app_state.set_current_user(user)
        return True
        
    # Registers a new user into the database.
    def register_user(self, password: str, first_name: str, last_name: str, email: str) -> bool:
        conn = self.db_service.connect()
        # Validates the connection.
        if conn is None:
            raise ValueError("Database connection failed.")
        
        # Validates passed in variables prior to pushing new user information to database.
        if not password:
            raise ValueError("Password Invalid.")
        if not first_name:
            raise ValueError("First Name Invalid")
        if not last_name:
            raise ValueError("Last Name Invalid")
        if not email:
            raise ValueError("Email Invalid")
        # Hashes the password passed in for secure storage in the database.
        hashed_password = self.auth_service.hash_password(password)

        # Verifies that there is not already an account under the same email provided.
        existing_user = self.db_service.get_user_by_email(email)
        if existing_user:
            raise ValueError("User already exists.")

        # Pushes the new user information to the database.
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hashed_password))
            conn.commit()
            self.portfolio_controller.create_portfolio(self.db_service.get_user_id(email))
            return True
        except Exception as e:
            print(e)
            raise RuntimeError("User registration failed.") from e
        finally:
            # Closes database connection and returns True for a successful user registration.
            conn.close()

    # Removes a user from the database.
    def remove_user(self, first_name: str, last_name: str, email: str) -> bool:
        pass