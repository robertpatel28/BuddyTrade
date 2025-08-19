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
from controllers.analysis_controller import AnalysisController
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import webbrowser


class HomeLoggedInController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager, analysis_controller: AnalysisController):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager
        self.analysis_controller = analysis_controller

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnAnalyzeTicker.clicked.connect(self.handle_analysis)
        self.ui.btnDashboard.clicked.connect(self.handle_dashboard)
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnAbout.clicked.connect(self.handle_about)
        self.ui.btnGitHub.clicked.connect(self.handle_github)
        self.ui.btnLinkedIn.clicked.connect(self.handle_linkedin)

    # Opens the home window (guest version)
    def handle_home(self):
        self.screen_manager.show_home_logged_in()

    # Method that opens the dashboard. Throws an error when called in this window as user is not logged in.
    def handle_dashboard(self):
        self.screen_manager.show_dashboard()
    
    # Method that opens the user / settings window.
    def handle_usersettings(self):
        None
        # IN PROGRESS

    # Opens the github profile.
    def handle_github(self):
        url = "https://github.com/robertpatel28"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    # Opens the linkedin profile.
    def handle_linkedin(self):
        url = "https://www.linkedin.com/in/robertpatel/"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    def handle_analysis(self):
        # Format ticker input to just the letters.
        ticker = self.ui.txtTickerSearch.text().strip()
        # Calls error method to show error to user.
        if not ticker:
            self.show_error("Invalid Input", "Please enter a ticker symbol.")
            return

        try:
            # Attempt to load analysis page.
            self.analysis_controller.load_analysis(ticker)
            self.screen_manager.show_analysis()

        except ValueError as e:
            # Catches invalid ticker / no price data
            self.show_error("Invalid Ticker", str(e))

        except Exception as e:
            # Catches unexpected errors
            self.show_error("Error", f"An unexpected error occurred: {str(e)}")

    def handle_faqs(self):
        None
        # IN PROGRESS

    def handle_about(self):
        url = "https://github.com/robertpatel28/BuddyTrade"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    def handle_support(self):
        None
        # IN PROGRESS

    # Helper method that shows error box with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    # Helper method that shows information box with given title and message.
    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)
