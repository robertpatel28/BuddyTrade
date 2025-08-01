#
# Author: Robert Patel
# This class represents the controller which connects the UI for the user registration window
# and the backend logic for registering a user.
#
# registration_controller.py
from PyQt6.QtWidgets import QMessageBox
from controllers.user_controller import UserController
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from PyQt6.QtWidgets import QMainWindow
from controllers.screen_manager import ScreenManager

class HomeLoggedInController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnDashboard.clicked.connect(self.handle_dashboard)
        self.ui.btnHome.clicked.connect(self.handle_home)

    # Opens the home window (guest version)
    def handle_home(self):
        self.screen_manager.show_home_logged_out()

    # Method that opens the dashboard. Throws an error when called in this window as user is not logged in.
    def handle_dashboard(self):
        self.screen_manager.show_dashboard()
    
    # Method that opens the user / settings window.
    def handle_usersettings(self):
        None
        # IN PROGRESS

    def handle_faqs(self):
        None
        # IN PROGRESS

    def handle_about(self):
        None
        # IN PROGRESS

    def handle_support(self):
        None
        # IN PROGRESS

    # Helper method that shows error box with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    # Helper method that shows information box with given title and message.
    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)
