#
# Author: Robert Patel
# This class is the controller which connects backend logic to the
# login screen for the user.
#

from PyQt6.QtWidgets import QMessageBox
from controllers.user_controller import UserController
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from controllers.screen_manager import ScreenManager
from PyQt6.QtWidgets import QMainWindow
from controllers.portfolio_controller import PortfolioController
from controllers.dashboard_controller import DashboardController
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class LoginController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager, portfolio_controller: PortfolioController, dashboard_controller: DashboardController):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager
        self.portfolio_controller = portfolio_controller
        self.dashboard_controller = dashboard_controller

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnLoginUser.clicked.connect(self.handle_login)
        self.ui.btnRegister.clicked.connect(self.handle_register)
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnDashboard.clicked.connect(self.handle_dashboard)
        self.ui.btnLogin.clicked.connect(self.handle_login_window)
        self.ui.btnAbout.clicked.connect(self.handle_about)
        self.ui.btnGitHub.clicked.connect(self.handle_github)

    def handle_login(self):
        email = self.ui.txtEmail.text().strip()
        password = self.ui.txtPassword.text().strip()

        try:
            success = self.user_controller.login_user(email, password)
            if success:
                user = self.db_service.get_user_by_email(email)
                portfolio = self.portfolio_controller.get_portfolio_by_user_id(self.db_service.get_user_id(email))

                self.app_state.set_current_user(user)
                self.app_state.set_current_portfolio(portfolio)

                self.screen_manager.show_dashboard()
                self.screen_manager.dashboard_controller.load_portfolio()
        except ValueError as e:
            self.show_error("Login Error", str(e))
        except Exception as e:
            self.show_error("Unexpected Error", str(e))

    # Opens the home window (guest version)
    def handle_home(self):
        self.screen_manager.show_home_logged_out()

    # Method that opens the dashboard. Throws an error when called in this window as user is not logged in.
    def handle_dashboard(self):
        self.show_error("Invalid User", "Must login to the application to access the 'Dashboard' tab.")

    # Method that opens the login window.
    def handle_login_window(self):
        self.screen_manager.show_login()

    # Method that opens the register window.
    def handle_register(self):
        self.screen_manager.show_register()

    # Opens the github profile.
    def handle_github(self):
        url = "https://github.com/robertpatel28"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

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

    # Helper method to display error box to user with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)
