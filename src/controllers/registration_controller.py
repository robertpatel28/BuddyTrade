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
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class RegistrationController:
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
        self.ui.btnRegister.clicked.connect(self.handle_register)
        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.btnDashboard.clicked.connect(self.handle_dashboard)
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnAbout.clicked.connect(self.handle_about)
        self.ui.btnGitHub.clicked.connect(self.handle_github)
        self.ui.btnLinkedIn.clicked.connect(self.handle_linkedin)

    def handle_register(self):
        email = self.ui.txtEmail.text().strip()
        verify_email = self.ui.txtVerifyEmail.text().strip()
        password = self.ui.txtPassword.text().strip()
        verify_password = self.ui.txtVerifyPassword.text().strip()
        first_name = self.ui.txtFirstName.text().strip()
        last_name = self.ui.txtLastName.text().strip()

        # Validation
        if email != verify_email:
            self.show_error("Email Mismatch", "Emails do not match.")
            return
        if password != verify_password:
            self.show_error("Password Mismatch", "Passwords do not match.")
            return

        try:
            success = self.user_controller.register_user(password, first_name, last_name, email)
            if success:
                self.show_info("Success", "Account successfully created!")
        except ValueError as e:
            self.show_error("Registration Error", str(e))
        except Exception as e:
            self.show_error("Unexpected Error", str(e))

    # Opens the home window (guest version)
    def handle_home(self):
        self.screen_manager.show_home_logged_out()

    # Method that opens the dashboard. Throws an error when called in this window as user is not logged in.
    def handle_dashboard(self):
        self.show_error("Invalid User", "Must login to the application to access the 'Dashboard' tab.")
    
    # Method that opens the login window.
    def handle_login(self):
        self.screen_manager.show_login()

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
